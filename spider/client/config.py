# -*- coding: utf-8 -*-

'''爬虫相关的配置信息
'''

import logging
import logging.handlers
import sys

#配置文件
CONFIG_FILE = r'config.ini'

#设置日志记录对象
LOG_FILE = 'log.txt'
LOG_FORMAT = '%(levelname)s %(asctime)-15s %(message)s'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
LOGGER = logging.getLogger()
fmt = logging.Formatter(LOG_FORMAT , DATE_FORMAT)
hdlr = logging.handlers.RotatingFileHandler(
              LOG_FILE, maxBytes=5000, backupCount=0)
hdlr.setFormatter(fmt)
LOGGER.addHandler(hdlr)
LOGGER.setLevel(logging.ERROR)
print >> sys.stderr,'logging ok.'
