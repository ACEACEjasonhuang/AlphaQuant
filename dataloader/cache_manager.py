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


class CacheManager(object):
    _tableSaved = {}        # 存储DataFrame
    _fieldsSaves = {}       # 记录各表已缓存字段
    _fieldsIndex = {}       # 记录每个字段对应的index
    _fieldsStkCnt = {}      # 记录每个字段对应的 日期 股票数量 dataFrame，应该为
    _calendar = None        #
    _stockCounts = None     # 所有日期 股票 对组合

    def __init__(self, cache_level=1, data_source='h5'):

        self._data_srouce = data_source
        self._cache_level = cache_level
        if self._data_srouce == 'h5':
            pass
        elif self._data_srouce == 'wind':
            self._loader = DataLoader()

    def _cache_calendar(self):
        """

        :return:
        """

        if CacheManager._calendar is None:
            CacheManager._calendar = Calendar()


