# -*- coding: utf-8 -*-
"""
-------------------------------------------------
# @Project  :AlphaQuant 
# @File     :module_test
# @Date     :2022/8/27 0027 18:23 
# @Author   :Junzhe Huang
# @Email    :acejasonhuang@163.com
# @Software :PyCharm
-------------------------------------------------
"""
from utils.logger import system_log, user_log

if __name__ == "__main__":
    system_log.info('INFO')
    system_log.debug('DEBUG')
    user_log.info('INFO')
    user_log.debug('DEBUG')
