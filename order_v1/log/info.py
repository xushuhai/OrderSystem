#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/14 14:33
# @Author  : Xsh
# @File    : info.py
# @Software: PyCharm

import logging

from config.test import LOG_LEVEL, LOG_NAME

numeric_level = getattr(logging, LOG_LEVEL.upper(), None)
if not isinstance(numeric_level, int):
    raise ValueError('Invalid log level:%s' % LOG_LEVEL)

FORMAT = '''%(asctime)s - %(module)s- %(lineno)d - %(message)s'''

logging.basicConfig(level=numeric_level, format=FORMAT)
logger = logging.getLogger(LOG_NAME)

fh = logging.FileHandler('%s.log' % (LOG_NAME), encoding='UTF-8')
fh.setFormatter(logging.Formatter(FORMAT))
logger.addHandler(fh)
#
# ch = logging.StreamHandler()
# logger.addHandler(ch)
logger.setLevel(numeric_level)
