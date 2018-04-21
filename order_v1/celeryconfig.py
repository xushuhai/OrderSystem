#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/15 09:59
# @Author  : Xsh
# @File    : celeryconfig.py
# @Software: PyCharm

from config.test import REDIS_URL_REPONSE, REDIS_URL_REQUEST
BROKER_URL = REDIS_URL_REQUEST
CELERY_RESULT_BACKEND = REDIS_URL_REPONSE