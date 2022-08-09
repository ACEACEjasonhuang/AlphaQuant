# -*- coding: utf-8 -*-
"""
-------------------------------------------------
# @Project  :AlphaQuant 
# @File     :debug_module
# @Date     :2022/7/26 15:23 
# @Author   :Junzhe Huang
# @Email    :acejasonhuang@163.com
# @Software :PyCharm
-------------------------------------------------
"""
from functools import wraps
import time
import signal


def time_cost(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        s = time.time()
        result = f(*args, **kwargs)
        e = time.time()
        print('[finished {func_name} in {time:.2f}s]'.format(func_name=f.__name__, time=e - s))
        return result
    return decorated
