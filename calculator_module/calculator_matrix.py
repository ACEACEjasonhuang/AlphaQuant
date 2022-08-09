# -*- coding: utf-8 -*-
"""
-------------------------------------------------
# @Project  :AlphaQuant 
# @File     :calculator_matrix
# @Date     :2022/7/26 16:23 
# @Author   :Junzhe Huang
# @Email    :acejasonhuang@163.com
# @Software :PyCharm
-------------------------------------------------
"""
import pandas as pd
import numpy as np


class CalculatorMatrix(object):
    """
    矩阵计算函数库：
    1.  用于减少groupby操作
    2. rowindex 时间 colindex 股票代码
    3.
    """

    def __init__(self):
        pass

    @classmethod
    def power(cls, x, n):
        return np.sign(x) * np.power(x.abs(), n)




