# -*- coding: utf-8 -*-
"""
-------------------------------------------------
# @Project  :AlphaQuant 
# @File     :cache_manager
# @Date     :2022/8/1 7:13 
# @Author   :Junzhe Huang
# @Email    :acejasonhuang@163.com
# @Software :PyCharm
-------------------------------------------------
"""
import os
import configparser as cp
from utils.calendar import Calendar
from dataloader.tushare_data import DataLoaderTuShare

class CacheManager(object):
    _table_saved = {}        # 存储DataFrame
    _fields_saves = {}       # 记录各表已缓存字段
    _fields_index = {}       # 记录每个字段对应的index
    _fields_stock_count = {}      # 记录每个字段对应的 日期 股票数量 dataFrame，应该为
    _calendar = None        #
    _stockCounts = None     # 所有日期 股票 对组合

    def __init__(self, cache_level=1, data_source='tushare'):
        """
        缓存初始化
        :param cache_level:
        :param data_source:
        """
        self._data_source = data_source
        self._cache_level = cache_level
        _upper_path, _file = os.path.split(os.path.realpath(__file__))
        _module_path, _ = os.path.split(_upper_path)
        cfp = cp.ConfigParser()
        if self._data_source == 'h5':
            pass
        elif self._data_source == 'tushare':
            cfp.read(os.path.join(_upper_path, 'configs', 'token.ini'))
            _token = dict(cfp.items("token"))
            self.ts_loader = DataLoaderTuShare(_token['default_token'])
        elif self._data_source == 'wind':
            pass
        else:
            raise ValueError("Wrong data_source param {}".format(self._data_source))

        self._cache_level = cache_level
        self._cache_calendar()
        self._cache_stock_counts()

    def _cache_calendar(self):
        """
        初始化类日期模块
        :return:
        """
        if CacheManager._calendar is None:
            CacheManager._calendar = Calendar()

    def _cache_stock_counts(self):
        """
        初始化类股票计数器
        :return:
        """
        pass

