# -*- coding: utf-8 -*-
"""
-------------------------------------------------
# @Project  :AlphaQuant 
# @File     :date_module
# @Date     :2022/8/12 0012 19:46 
# @Author   :Junzhe Huang
# @Email    :acejasonhuang@163.com
# @Software :PyCharm
-------------------------------------------------
"""
from datetime import datetime, timedelta


class DateTools(object):
    @staticmethod
    def shift_quarter(date, n=1):
        """
        移动若干个季度，默认向后移动
        :param date: 初始季度 ['0331', '0630', '0930', '1231']
        :param n: 大于0 向后移动
        :return:
        """
        _quarter_list = ['0331', '0630', '0930', '1231']
        if date[4:] not in _quarter_list:
            raise ValueError('IN FUNCTION _shift_quarter ERROR param')
        if n == 0:
            return date
        if n < 0:
            if date[4:] == '0331':
                res = "{}{}".format(int(date[:4]) - 1, '1231')
            else:
                res = "{}{}".format(date[:4], _quarter_list[_quarter_list.index(date[4:]) - 1])
            return DateTools.shift_quarter(res, n + 1)
        else:
            if date[4:] == '1231':
                res = "{}{}".format(int(date[:4]) + 1, '0331')
            else:
                res = "{}{}".format(date[:4], _quarter_list[_quarter_list.index(date[4:]) + 1])
            return DateTools.shift_quarter(res, n - 1)

    @staticmethod
    def shift_year(date, n):
        """
        移动若干年，默认向前移动
        :param date:
        :param n:
        :return:
        """
        return "{}{}".format(int(date[:4]) + n, date[4:])

    @staticmethod
    def shift_day(date, n):
        """
        移动若干日，默认向前移动
        :param date:
        :param n:
        :return:
        """
        _date = datetime.strptime(date, '%Y%m%d')
        _date = _date + timedelta(days=n)
        return _date.strftime('%Y%m%d')

    @staticmethod
    def report_date_now():
        dt = datetime.now().strftime('%Y%m%d')
        if dt[4:] < '0430':
            __res = str(int(dt[:4]) - 1) + '0630'
        elif dt[4:] < '0830':
            __res = str(int(dt[:4]) - 1) + '1231'
        else:
            __res = dt[:4] + '0630'
        return __res


