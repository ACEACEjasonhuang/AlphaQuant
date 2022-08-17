# -*- coding: utf-8 -*-
"""
-------------------------------------------------
# @Project  :AlphaQuant 
# @File     :factor_base
# @Date     :2022/8/16 0016 4:43 
# @Author   :Junzhe Huang
# @Email    :acejasonhuang@163.com
# @Software :PyCharm
-------------------------------------------------
"""
import pandas as pd
import numpy as np

import time
import os


class FactorBase(object):

    data_loader = None
    factor_IO = None
    factor_risk = None

    def __init__(self):
        self.need_field = None
        self.need_table_fields = None

    def factor_def(self):
        raise NotImplementedError

    def run(self):
        """

        :return:
        """
