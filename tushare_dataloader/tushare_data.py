# -*- coding: utf-8 -*-
"""
-------------------------------------------------
# @Project  :AlphaQuant 
# @File     :tushare_data_new
# @Date     :2022/8/12 0012 17:09 
# @Author   :Junzhe Huang
# @Email    :acejasonhuang@163.com
# @Software :PyCharm
-------------------------------------------------
"""
from math import ceil
import time
import pandas as pd
import numpy as np
import tushare as ts
from functools import wraps
from dataloader.constants import TuShareStockDataDaily, DefaultTime, SaveStockDataDaily, SaveDataSet
from utils.date_module import DateTools
import configparser as cp
from collections import Counter
import os


class DataLoaderTuShare(object):
    def __init__(self, ts_token=None):
        """
        :param ts_token: tushare token 默认读取配置文件
        """
        if ts_token is None:
            # 读取配置文件中的token
            _upper_path, _file = os.path.split(os.path.realpath(__file__))
            _module_path, _ = os.path.split(_upper_path)
            cfp = cp.ConfigParser()
            cfp.read(os.path.join(_upper_path, 'configs', 'token.ini'))
            ts_token = dict(cfp.items("token"))
        self._ts = ts
        self._ts.set_token(ts_token)
        self.pro = ts.pro_api(ts_token)
        self._cnt = 0
        self.start_bar_time = 0
        self._default_start_time = DefaultTime.DEFAULT_START_TIME
        self._default_end_time = DefaultTime.DEFAULT_END_TIME

    def pro_bar_safe_daily(self, limit_size=5000, *args, **kwargs):
        """
        多次提取防止条数限制
        :param limit_size: 限制条数
        :param args:
        :param kwargs:
        :return:
        """
        assert ('start_date' in kwargs) and ('end_date' in kwargs)
        start_time = kwargs['start_date']
        end_time = kwargs['end_date']
        kwargs.pop('start_date')
        kwargs.pop('end_date')
        gap_year = limit_size // 252 - 1

        def split_year(_start_time, _end_time, gap_year):
            _split_year = []
            _temp_date_1, _temp_date_2= _start_time, DateTools.shift_year(_start_time, gap_year)
            while _temp_date_2 < _end_time:
                _split_year.append((_temp_date_1, _temp_date_2))
                _temp_date_1 = DateTools.shift_day(_temp_date_2, 1)
                _temp_date_2 = DateTools.shift_year(_temp_date_1, gap_year)
            _split_year.append((_temp_date_1, _end_time))
            return _split_year
        # 避免日期重复
        _temp1 = [self._ts.pro_bar(start_date=_start,
                                   end_date=_end,
                                   *args,
                                   **kwargs
                                   ) for _start, _end in split_year(start_time, end_time, gap_year)]

        __res = pd.concat(_temp1)
        return __res

    def get_history_daily_data(self, code, asset='E', adj='hfq', start_time=None, end_time=None):
        """
        获取历史日线数据
        :param adj: 前复权 or 后复权 默认后复权
        :param code: 资产代码
        :param freq: 频率 ：['5min', '30min', '60min', '1d'] 默认 D
        :param asset: 资产类别 E股票（默认） I沪深指数 C数字货币 FT期货 FD基金 O期权 CB可转债
        :param asset: 复权类型 None未复权 qfq前复权 hfq后复权 , 默认后复权
        :param start_time: 包含
        :param end_time: 包含
        :return:
        """
        if not start_time:
            start_time = self._default_start_time
        if not end_time:
            end_time = self._default_end_time
        default_field = TuShareStockDataDaily.get_values()
        _dict_ts = TuShareStockDataDaily.get_attr()
        _dict_save = SaveStockDataDaily.get_attr()
        _field_map = {_dict_ts[i]: _dict_save[i] for i in _dict_ts}

        time_col = TuShareStockDataDaily.TRADE_DT
        if isinstance(code, str):
            code = [code]
        __df_set = []
        for _code in code:
            temp_df = self.pro_bar_safe_daily(ts_code=_code, asset=asset, start_date=start_time,
                                              adj=adj,
                                              end_date=end_time,
                                              freq='D')
            if len(temp_df) != 0:
                __df_set.append(temp_df.sort_values(time_col))

        if len(__df_set) == 0:
            __res = pd.DataFrame(columns=default_field)
            return __res
        __res = pd.concat(__df_set)
        __res.reset_index(drop=True, inplace=True)
        __res.rename(columns=_field_map, inplace=True)
        __res.set_index([SaveStockDataDaily.TRADE_DT, SaveStockDataDaily.STOCK_CODE], inplace=True)
        return __res

    def get_stock_basic(self, ts_code=None, is_hs=None, list_status=None, exchange=None, market=None):
        """
        :param ts_code: 股票代码
        :param is_hs: 是否沪深股票
        :param list_status: 上市状态
        :param exchange: 交易所
        :param market: 市场
        :return:
        """
        _data = self.pro.stock_basic(ts_code=ts_code, is_hs=is_hs, list_status=list_status,
                                     exchange=exchange, market=market,
                                     fields='ts_code,name,industry,market,exchange,is_hs,list_date,delist_date')
        return _data

    def get_calendar(self, exchange=None, start_date='20000101', end_date='20991231'):
        return self.pro.trade_cal(exchange=exchange, start_date=start_date, end_date=end_date, is_open='1')

    def get_stock_number(self, save_to_h5=False):
        """
        获取当天上市股票总数
        :param save_to_h5:
        :return:
        """
        _upper_path, _file = os.path.split(os.path.realpath(__file__))
        _module_path, _ = os.path.split(_upper_path)
        cfp = cp.ConfigParser()
        cfp.read(os.path.join(_module_path, 'configs', 'data_path.ini'))
        _relative_data_path = dict(cfp.items("data"))
        _real_data_path = os.path.join(_module_path, _relative_data_path['constants'],
                                       '{}{}'.format(SaveDataSet.STOCK_DAILY_COUNT, '.h5'))

        # 根据股票上市和退市日期，获取当日上市总股票数量
        _calendar = self.get_calendar()
        _start_date, _end_date = min(_calendar['cal_date']), max(_calendar['cal_date'])
        _stk_basic = self.get_stock_basic()
        _list_date = _stk_basic['list_date']
        _list_date = np.where(_list_date <= _start_date, _start_date, _list_date)
        _ser_list_date = pd.Series(dict(Counter(_list_date)))
        _delist_date = _stk_basic[_stk_basic['delist_date'].notna()]
        _delist_date = np.where(_delist_date <= _start_date, _start_date, _delist_date)
        _ser_delist_date = pd.Series(dict(Counter(_delist_date)))
        _temp_df = pd.DataFrame({'list_number': _ser_list_date, 'delist_number': _ser_delist_date}).fillna(0).cumsum()
        _stk_number = pd.DataFrame(index=_calendar['cal_date'])
        _stk_number[SaveDataSet.STOCK_DAILY_COUNT] = (_temp_df['list_number'] - _temp_df['delist_number']).astype(int)
        _stk_number.fillna(method='ffill', inplace=True)

        if save_to_h5:
            _stk_number.to_hdf(path_or_buf=_real_data_path, mode='w', key=SaveDataSet.STOCK_DAILY_COUNT)
        return _stk_number


    def test(self):
        """
        测试单元
        :return:
        """
        __res = self.get_stock_number(save_to_h5=True)
        print(__res)


if __name__ == '__main__':
    _token = '9f22d4042f10a22eb142bef09a1b31e8d6807f276d902863fe771167'
    loader = DataLoaderTuShare(_token)
    loader.test()
    # print(loader.get_history_daily_data(['000001.SZ', '000002.SZ']))