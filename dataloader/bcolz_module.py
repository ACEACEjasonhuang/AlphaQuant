# -*- coding: utf-8 -*-
# @Time     : 2024/5/31
# @Author   : Junzhe Huang
# @Email    : huangjz01@igoldenbeta.com
# @File     : bcolz_module
# @Software : AlphaQuant


import bcolz
import os


# bcolz数据读取、写入、创建、删除
class BcolzModule(object):
    @staticmethod
    def read_stock_bcolz_data(path, start_date=None, end_date=None, sec_list=None, field_list=None):
        """
        读取股票bcolz数据
        :param path: bcolz数据路径
        :param start_date: 开始日期
        :param end_date: 结束日期
        :param sec_list: 证券列表
        :param field_list: 字段列表
        """
        return bcolz.open(path)

    @staticmethod
    def write_bcolz_data(data, path):
        """
        写入bcolz数据
        :param data: bcolz数据
        :param path: bcolz数据路径
        :return: None
        """
        data.todata(path)

    @staticmethod
    def create_bcolz_data(data, path):
        """
        创建bcolz数据
        :param data: bcolz数据
        :param path: bcolz数据路径
        :return: None
        """
        bcolz.carray(data).todata(path)

    @staticmethod
    def remove_bcolz_data(path):
        """
        删除bcolz数据
        :param path: bcolz数据路径
        :return: None
        """
        os.remove(path)