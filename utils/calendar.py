# -*- coding: utf-8 -*-
"""
-------------------------------------------------
# @Project  :AlphaQuant 
# @File     :calendar
# @Date     :2022/8/1 9:52 
# @Author   :Junzhe Huang
# @Email    :acejasonhuang@163.com
# @Software :PyCharm
-------------------------------------------------
"""
# todo: init & _load_trade_date: 多个数据源

import numpy as np
import pandas as pd
from functools import partial
from datetime import datetime


class Calendar(object):
    _trade_dates = None
    head_date = None
    tail_date = None

    def __init__(self, data_source='h5'):
        self._data_source = data_source
        if self._data_source == 'wind':
            pass
        elif self._data_source == 'h5':
            pass
        else:
            raise ValueError('Wrong Data Source {}'.format(self._data_source))

        self._load_trade_dates()

    def _load_trade_dates(self):
        """
        载入交易日期序列
        :return:
        """
        if Calendar._trade_dates is None:
            if self._data_source == 'wind':
                pass
            elif self._data_source == 'h5':
                pass
            else:
                raise ValueError('Wrong Data Source {}'.format(self._data_source))

    def _calibrate_date(self, curr_date, curr_side='left'):
        """
        返回最近交易日
        :param curr_date:
        :param curr_side:
        :return:
        """
        curr_date = str(curr_date)
        if curr_date not in self._trade_dates:
            if curr_date > self._trade_dates[-1]:
                curr_date = self._trade_dates[-1]
            elif curr_date < self._trade_dates[0]:
                curr_date = self._trade_dates[0]
            else:
                curr_date = self._trade_dates[self._trade_dates < curr_date][-1] \
                    if curr_side == 'left' \
                    else self._trade_dates[self._trade_dates > curr_date][0]
        return curr_date

    def t_days_offset(self, num, curr_dates, curr_side='left'):
        """
        计算根基curr_date 日期， 移动 num 日 所得到的 交易日
        :param num:
        :param curr_dates:
        :param curr_side: 若非交易日，则取左或者右
        :return:
        """
        single_date = False
        if not (isinstance(curr_dates, np.ndarray)) or isinstance(curr_dates, list):
            single_date = True
            curr_dates = np.array([str(curr_dates)])
        total_day_num = self._trade_dates.shape[0]
        curr_dates = list(map(partial(self._calibrate_date, curr_side=curr_side), curr_dates))
        curr_pos = np.array(curr_dates) + num
        curr_pos = np.where(curr_pos < 0, 0, curr_pos)
        curr_pos = np.where(curr_pos > total_day_num - 1, total_day_num - 1, curr_pos)
        offset_dates = self._trade_dates[curr_pos]
        return offset_dates[0] if single_date else offset_dates

    def t_days_count(self, head_date, tail_date, select_type='CO'):
        """
        计算期间天数
        :param head_date:
        :param tail_date:
        :param select_type:‘CO’:前闭后开区  ‘OO’:前开后开-1   ‘CC’:前闭后闭 + 1
        :return:
        """
        t_days_between = self.t_days_between(head_date, tail_date, select_type)
        return len(t_days_between)

    def t_days_between(self, head_date, tail_date, select_type='CO'):
        """
        返回期间交易日序列
        :param head_date:
        :param tail_date:
        :param select_type:
        :return:
        """
        if not isinstance(head_date, str):
            head_date = str(head_date)
        if not isinstance(tail_date, str):
            head_date = str(tail_date)
        if head_date > tail_date:
            # log 错误
            return pd.DataFrame(columns=['DATE'])

        if select_type == 'CO':
            _index = (self._trade_dates >= head_date) & (self._trade_dates < tail_date)
        elif select_type == 'OC':
            _index = (self._trade_dates > head_date) & (self._trade_dates <= tail_date)
        elif select_type == 'CC':
            _index = (self._trade_dates >= head_date) & (self._trade_dates <= tail_date)
        elif select_type == 'OO':
            _index = (self._trade_dates > head_date) & (self._trade_dates < tail_date)
        else:
            raise ValueError("WRONG SELECT TYPE")
        return self._trade_dates.loc[_index, :]

    def t_ends_between(self, head_date, tail_date, period_type='tail', gap_type='month', gap_len=12):
        """
        提取不同周期的末端 交易日
        :param head_date:
        :param tail_date:
        :param period_type: return date , head / tail of the period
        :param gap_type: year quarter week
        :param gap_len: 间隔数个月
        :return:
        """
        _between_days = self.t_days_between(head_date=head_date, tail_date=tail_date, select_type="CC")

        if len(_between_days) <= 1:
            return _between_days
        if gap_type == 'year':
            date_mark = np.array([int(_date[:4]) for _date in _between_days])
        elif gap_type == 'quarter':
            date_mark = np.array([(int(_date[4:6]) - 1) // 3 for _date in _between_days])
        elif gap_type == 'month':
            date_mark = np.array([int(_date[4:6]) for _date in _between_days])
        elif gap_type == 'week':
            # 返回周序号
            date_mark = np.array([int(datetime.strptime(_date, '%Y%m%d').strftime("%W")) for _date in _between_days])
        else:
            raise ValueError("WRONG GAP TYPE")

        # 取区间首还是区间尾
        ret_head = period_type == 'head'
        if ret_head:
            diff_pos = np.concatenate([[1], np.diff(date_mark) != 0])
        else:
            diff_pos = np.concatenate([np.diff(date_mark) != 0, [0]])
        if gap_len == 1:
            cut_dates = _between_days[diff_pos > 0]
        else:
            mod_val = 1 if ret_head else 0
            cut_dates = _between_days[((np.cumsum(diff_pos) % gap_len) == mod_val) & (diff_pos > 0)]

        # 加上起始和结束日期
        first_date = _between_days[0]   # 不一定是head_date
        last_date = _between_days[-1]   # 不一定是tail_date
        if cut_dates.shape[0] == 0:     # 可能在取tail的时候出现
            cut_dates = [first_date, last_date]
        else:
            if first_date < cut_dates[0]:
                cut_dates = np.concatenate([[first_date], cut_dates])
            if last_date > cut_dates[-1]:
                cut_dates = np.concatenate([cut_dates, [last_date]])

        return cut_dates