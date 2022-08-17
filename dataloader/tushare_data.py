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
import tushare as ts
from functools import wraps
from constants import TuShareDataDaily, DefaultTime, SaveDataDaily
from utils.date_module import DateTools


class DataLoaderTuShare(object):
    def __init__(self, ts_token):
        """

        :param ts_token: tushare token
        """
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
        default_field = TuShareDataDaily.get_values()
        _dict_ts = TuShareDataDaily.get_attr()
        _dict_save = SaveDataDaily.get_attr()
        _field_map = {_dict_ts[i]: _dict_save[i] for i in _dict_ts}

        time_col = TuShareDataDaily.TRADE_DT
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
        __res.set_index([SaveDataDaily.TRADE_DT, SaveDataDaily.STOCK_CODE], inplace=True)
        return __res


if __name__ == '__main__':
    ts_token = '9f22d4042f10a22eb142bef09a1b31e8d6807f276d902863fe771167'
    loader = DataLoaderTuShare(ts_token)
    # print(loader.get_history_daily_data(['000001.SZ', '000002.SZ']))
    import os
    import configparser as cp
    print(__file__)
    upper_path, _file = os.path.split(os.path.realpath(__file__))
    module_path, _ = os.path.split(upper_path)
    cfp = cp.ConfigParser()
    cfp.read(os.path.join(module_path, 'configs', 'token.ini'))
    print(dict(cfp.items("token")))