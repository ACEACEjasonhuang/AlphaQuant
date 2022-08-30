# -*- coding: utf-8 -*-
"""
-------------------------------------------------
# @Project  :AlphaQuant 
# @File     :logger
# @Date     :2022/8/26 0026 8:25 
# @Author   :Junzhe Huang
# @Email    :acejasonhuang@163.com
# @Software :PyCharm
-------------------------------------------------
"""
import os
import logbook
from logbook import Logger, TimedRotatingFileHandler
from logbook.more import ColorizedStderrHandler

# patch warn
logbook.base._level_names[logbook.base.WARNING] = 'WARN'

# 限制导出
__all__ = [
    'user_log',
    'system_log'
]

DATETIME_FORMAT = '%Y-%m_5d %H:%M:%S.%f'


def user_log_processor(record):
    pass


user_log_group = logbook.LoggerGroup(processor=user_log_processor)

# user_log
user_log = Logger('user_log')
user_log_group.add_logger(user_log)

# system_log
system_log = Logger('system_log')


def log_type(record, handler):
    log = "[{dt}][{level}][{filename}][{func_name}][{lineno}] {msg}".format(
        dt=record.time,
        level=record.level_name,
        filename=os.path.split(record.filename)[-1],
        func_name=record.func_name,
        lineno=record.lineno,
        msg=record.msg
    )
    return log


# 若主工程下没有logs文件夹，默认调试模式，日志只打印不输出
LOG_DIR = os.path.join('logs')
logbook.set_datetime_format("local")  # 设置时区格式为本地
user_log.handlers = []
system_log.handlers = []
if not os.path.exists(LOG_DIR):
    # 调试模式
    print("***********LOG****DEBUG METHOD************")
    log_std = ColorizedStderrHandler(bubble=True)
    log_std.formatter = log_type
    user_log.handlers.append(log_std)
    system_log.handlers.append(log_std)
else:
    # 运行模式
    user_log_file_handler = TimedRotatingFileHandler(os.path.join(LOG_DIR, '%s.log' % 'user_log'),
                                                     date_format='%Y%m%d', bubble=True)
    system_log_file_handler = TimedRotatingFileHandler(os.path.join(LOG_DIR, '%s.log' % 'system_log'),
                                                       date_format='%Y%m%d', bubble=True)
    user_log_file_handler.formatter = log_type
    system_log_file_handler.formatter = log_type
    user_log.handlers.append(user_log_file_handler)
    system_log.handlers.append(system_log_file_handler)
    # 运行模式不打印debug信息

    def void_func(*args, **kwargs):
        pass

    user_log.debug = void_func
    system_log.debug = void_func
