# -*- coding: utf-8 -*-
"""
-------------------------------------------------
# @Project  :AlphaQuant 
# @File     :calculator
# @Date     :2022/7/26 14:14 
# @Author   :Junzhe Huang
# @Email    :acejasonhuang@163.com
# @Software :PyCharm
-------------------------------------------------
"""
import pandas as pd
import numpy as np
from utils.debug_module import time_cost

class Calculator(object):
    """
        基础计算函数 ：
        1 所有输入数据为 以股票代码、日期 为multiindex 的 pd.DataFrame
        2 返回值应为 形状完全相同的 以股票代码、日期 为multiindex 的 pd.DataFrame
        3.对于数据中的缺失值，基本的处理思想是尽量保持原有数据提供的信息，如 计算五日均值
          数据有缺失 [1,2,nan,nan,3] 则使用其中有的三天数据进行计算
    """

    def __init__(self):
        pass

    @staticmethod
    def _trans_data(x, ret_df=False):
        # Series 和 DataFrame互相转换
        if ret_df:
            return x.to_frame() if isinstance(x, pd.Series) else x
        else:
            return x.iloc[:, 0] if isinstance(x, pd.DataFrame) else x

    @classmethod
    def cmp_min(cls, x, y, ret_df=False):
        # 组合两个Series， 取较小值
        _ser = pd.Series(np.where(x < y, x, y), index=x.index)
        return cls._trans_data(x=_ser, ret_df=ret_df)

    @classmethod
    def cmp_max(cls, x, y, ret_df=False):
        # 组合两个Series， 取较大值
        _ser = pd.Series(np.where(x > y, x, y), index=x.index)
        return cls._trans_data(x=_ser, ret_df=ret_df)

    @classmethod
    def delay(cls, x, num, by, fill_na=None, ret_df=False):
        # 滞后n期
        x = cls._trans_data(x, ret_df)
        ret = x.groupby(level=[by], sort=False, as_index=~ret_df, group_keys=False).shift(period=num)
        if fill_na is not None:
            ret[ret.isnull()] = fill_na
        return ret

    @classmethod
    def diff(cls, x, num, by, fill_na=None, ret_df=False):
        # n期差分
        x = cls._trans_data(x, ret_df)
        ret = x - cls.delay(x=x, num=num, by=by, fill_na=fill_na, ret_df=ret_df)
        return ret

    @classmethod
    def moving_max(cls, x, num, by, minopt=0, ret_df=False):
        # 获取滑动最大值序列
        x = cls._trans_data(x=x, ret_df=ret_df)
        ret = x.groupby(level=[by], sort=False, as_index=~ret_df, group_keys=False)\
            .rolling(window=num, min_periods=minopt).max()
        ret = ret.sort_index()
        return ret

    @classmethod
    def moving_min(cls, x, num, by, minopt=0, ret_df=False):
        # 获取滑动最小值序列
        x = cls._trans_data(x=x, ret_df=ret_df)
        ret = x.groupby(level=[by], sort=False, as_index=~ret_df, group_keys=False) \
            .rolling(window=num, min_periods=minopt).min()
        ret = ret.sort_index()
        return ret

    @classmethod
    def moving_mean(cls, x, num, by, minopt=0, ret_df=False):
        # 获取滑动平均值序列
        x = cls._trans_data(x=x, ret_df=ret_df)
        ret = x.groupby(level=[by], sort=False, as_index=~ret_df, group_keys=False) \
            .rolling(window=num, min_periods=minopt).mean()
        ret = ret.sort_index()
        return ret

    @classmethod
    def test_time(cls, fun1, fun2, *args, **kwargv):
        f1 = time_cost(fun1)
        f2 = time_cost(fun2)
        f1(*args, **kwargv)
        f2(*args, **kwargv)

    @classmethod
    def test1(cls, a, b):
        np.array([np.sum()])
        return a

    @classmethod
    def test2(cls, a, b):
        a[a < 0.5] = 0
        return a




if __name__ == "__main__":
    a = pd.Series(np.random.random(10000000))
    b = pd.Series(np.random.random(10000000))
    Calculator.test_time(Calculator.test1, Calculator.test2, a, b)
