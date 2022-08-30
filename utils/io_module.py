# -*- coding: utf-8 -*-
"""
-------------------------------------------------
# @Project  :AlphaQuant 
# @File     :io_module
# @Date     :2022/8/26 0026 8:03 
# @Author   :Junzhe Huang
# @Email    :acejasonhuang@163.com
# @Software :PyCharm
-------------------------------------------------
"""
import os
import configparser as cp


class IoModule(object):
    @staticmethod
    def get_path(_type, _subtype):
        _upper_path, _file = os.path.split(os.path.realpath(__file__))
        _module_path, _ = os.path.split(_upper_path)
        cfp = cp.ConfigParser()
        cfp.read(os.path.join(_module_path, 'configs', 'data_path.ini'))
        if cfp.has_section(_type):
            _data_path = dict(cfp.items(_type))
            if _subtype in _data_path:
                return os.path.join(_module_path, _data_path['constants'])
            else:
                raise ValueError("PATH WRONG:Subtype {} not in Section {}".format(_subtype, _type))
        else:
            raise ValueError("PATH WRONG:Section {} not in data_path.ini".format(_type))


if __name__ == '__main__':
    print(IoModule.get_path('data', 'constants'))
