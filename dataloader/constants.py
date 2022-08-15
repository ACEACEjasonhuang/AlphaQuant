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


class SaveDataDaily(Base):
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


class TuShareDataDaily(Base):
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


if __name__ == "__main__":
    print(TuShareDataDaily.get_values())