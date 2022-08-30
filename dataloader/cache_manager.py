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
import pandas as pd
from utils.calendar import Calendar
from tushare_dataloader.tushare_data import DataLoaderTuShare
from constants import SaveDataSet, cache_levels, SaveStockDataDaily
from utils.io_module import IoModule
from utils.logger import system_log, user_log


class CacheManager(object):
    """
    缓存数据管理
    """
    _table_saved = {}        # 存储DataFrame
    _fields_saved = {}       # 记录各表已缓存字段
    _fields_index = {}       # 记录每个字段对应的index
    _fields_stock_count = {}  # 记录每个字段对应的 日期 股票数量 dataFrame，应该为
    _calendar = None         #
    _stock_counts = None     # 所有日期 股票 对组合
    # 日期和股票数量的dataFrame

    def __init__(self, cache_level=1, data_source='tushare'):
        """
        缓存初始化
        :param cache_level:
        :param data_source:
        """
        self._data_source = data_source
        self._cache_level = cache_level
        if self._data_source == 'h5':
            pass
        elif self._data_source == 'tushare':
            self.ts_loader = DataLoaderTuShare()
        elif self._data_source == 'wind':
            pass
        else:
            system_log.error("Wrong data_source param {} for cache manager".format(self._data_source))
            raise ValueError("Wrong data_source param {}".format(self._data_source))

        self._cache_level = cache_level
        self._cache_calendar()
        self._cache_stock_counts()

    @classmethod
    def _cache_calendar(cls):
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
        if CacheManager._stock_counts is None:
            if self._data_source == 'tushare':
                CacheManager._stock_counts = self.ts_loader.get_stock_number()
            elif self._data_source == 'h5':
                _data_path = os.path.join(IoModule.get_path('data', 'constants'),
                                          '{}{}'.format(SaveDataSet.STOCK_DAILY_COUNT, '.h5'))
                CacheManager._stock_counts = \
                    pd.read_hdf(path_or_buf=_data_path, key=SaveDataSet.STOCK_DAILY_COUNT, mode='r')
            elif self._data_source == 'wind':
                pass

    def _check_in_cache(self, table_name, table_data, sort_table=True):
        """

        :param table_name:
        :param table_data:
        :param sort_table:
        :return:
        """
        if table_data.empty:
            system_log.error('Given table {} is empty, will not be cached'.format(table_name))
        index_fields = [SaveStockDataDaily.STOCK_CODE, SaveStockDataDaily.TRADE_DT]
        table_name = table_name.upper()
        cache_candidable = False
        for level in cache_levels:
            if table_name in cache_levels[level]:
                cache_candidable = True
                if level <= self._cache_level: # 符合缓存级别
                    system_log.info("{} : cache level {} wil;l be saved in cache".format(table_name, level))
                    data_index = table_data.index
                    # 不包含在index_field的column, 不包含股票代码和时间
                    data_field = [_col for _col in table_data.column if _col not in index_fields]
                    # 计算表中，每个字段，每日的股票数量， 包含空值
                    _table_stock_counts = table_data.groupby(level=SaveStockDataDaily.TRADE_DT, sort=False).count() + \
                                          table_data.isna().groupby(level=SaveStockDataDaily.TRADE_DT, sort=False).sum()

                    # 表第一次被缓存
                    if table_name not in self._table_saved:
                        self._table_saved[table_name] = table_data  # 缓存数据表
                        self._fields_saved[table_name] = data_field  # 缓存fields
                        # 对每一个field, 缓存数据表的index
                        self._fields_index[table_name] = {_field: data_index for _field in data_field}
                        # 缓存每个字段对应的每日股票数量
                        self._fields_stock_count[table_name] = {_field: _table_stock_counts.loc[:, [_field]]
                                                                for _field in data_field}
                        if sort_table:
                            self._table_saved[table_name].sort_index(inplace=True)

                        system_log.info('new table {} cached, fields {} with {} obs'
                                        .format(table_name, ','.join(data_field), table_data.shape[0]))

                    else:  # 已被缓存过的数据表
                        # 拆分已有和新的field
                        common_fields = [_field for _field in data_field if _field in self._fields_saved[table_name]]
                        new_field = [_field for _field in data_field if _field not in self._fields_saved[table_name]]
                        if new_field:  # 如果有新的字段
                            # 原始表与新字段外连接
                            self._table_saved[table_name] = self._table_saved[table_name]\
                                .join(other=table_data.loc[:, new_field], how='outer')
                            self._fields_saved[table_name].extend(new_field)
                            self._fields_index.update({_field: data_index for _field in new_field})
                            self._fields_stock_count.update({_field: _table_stock_counts.loc[:, [_field]]
                                                             for _field in new_field})
                        if common_fields:  # 共同字段 逐个字段处理
                            for _field in common_fields:
                                saved_index = self._fields_index[table_name][_field]
                                # 新数据和已存在表index差集， 空表示没有需要缓存的新数据
                                extra_index = data_index.difference(other=saved_index)
                                if not extra_index.empty:  # 需要延长数据表
                                    not_saved_extra_index =
                                    self._table_saved[table_name] = pd.concat([table_data.loc[]])

                        system_log.info('existing table {} cached, new')


if __name__ == "__main__":
    cm = CacheManager()





