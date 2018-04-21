#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/15 09:59
# @Author  : Xsh
# @File    : celeryconfig.py
# @Software: PyCharm

from kombu import Queue
from config.test import REDIS_URL_REPONSE, REDIS_URL_REQUEST

BROKER_URL = REDIS_URL_REQUEST
CELERY_RESULT_BACKEND = REDIS_URL_REPONSE

CELERY_DEFAULT_QUEUE = 'default'
CELERY_QUEUES = (
    Queue('default', routing_key='default'),
    Queue('sub_push', routing_key='sub_push'),
    )

CELERY_ROUTES = {
    'push.tasks.create_user_send_sms':{
        'queue':'sub_push',
        'routing_key':'sub_push',
    }
}