# -*- coding: utf-8 -*-
"""
-------------------------------------------------
# @Project  :AlphaQuant 
# @File     :constants
# @Date     :2022/8/12 0012 16:48 
# @Author   :Junzhe Huang
# @Email    :acejasonhuang@163.com
# @Software :PyCharm
-------------------------------------------------
"""


class Base(object):
    """
    加入方法可以返回所有定义的类型
    """
    @classmethod
    def get_attr(cls):
        params = {}
        for name in dir(cls):
            value = getattr(cls, name)
            if not name.startswith('__') and not callable(value):
                params[name] = value
        return params

    @classmethod
    def get_keys(cls):
        _dict = cls.get_attr()
        return list(_dict.keys())

    @classmethod
    def get_values(cls):
        _dict = cls.get_attr()
        return list(_dict.values())


class DefaultTime(Base):
    DEFAULT_START_TIME = '20001201'
    DEFAULT_END_TIME = '20211231'


class SaveStockDataDaily(Base):
    TRADE_DT = 'TRADE_DT'
    STOCK_CODE = 'STOCK_CODE'
    OPEN = 'OPEN'
    HIGH = 'HIGH'
    LOW = 'LOW'
    CLOSE = 'CLOSE'
    PRE_CLOSE = 'PRE_CLOSE'
    CHANGE = 'CHANGE'
    PCT_CHANGE = 'PCT_CHANGE'
    VOLUME = 'VOLUME'
    AMOUNT = 'AMOUNT'


class TuShareStockDataDaily(Base):
    TRADE_DT = 'trade_date'
    STOCK_CODE = 'ts_code'
    OPEN = 'open'
    HIGH = 'high'
    LOW = 'low'
    CLOSE = 'close'
    PRE_CLOSE = 'pre_close'
    CHANGE = 'change'
    PCT_CHANGE = 'pct_chg'
    VOLUME = 'vol'
    AMOUNT = 'amount'


class TuShareStockBasic(Base):
    STOCK_CODE = 'ts_code'
    STOCK_NAME = 'name'
    AREA = 'area'
    INDUSTRY = 'industry'
    STOCK_FULLNAME = 'fullname'
    MARKET_TYPE = 'market'
    EXCHANGE = 'exchange'
    CURRENT_TYPE = 'curr_type'
    LIST_STATUS = 'list_status'
    LIST_DATE = 'list_date'
    DELIST_DATE = 'delist_date'
    IS_HS = 'is_hs'


class TuShareCalendar(Base):
    EXCHANGE = 'exchange'
    START_DATE = 'start_date'
    END_DATE = 'end_date'
    IS_OPEN = 'is_open'
    CAL_DATE = 'cal_date'
    PRE_TRADE_DATE = 'pretrade_date'



if __name__ == "__main__":
    print(TuShareStockDataDaily.get_values())