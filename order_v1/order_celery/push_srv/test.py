#!/usr/bin/env python
# -*- coding: utf-8 -*-cele
# @Time    : 2017/12/15 15:21
# @Author  : Xsh
# @File    : test.py
# @Software: PyCharm

import json
import random
from celery import Celery

celery = Celery()
celery.config_from_object('celeryconfig')

if __name__ == '__main__':
    my_str = ''
    for i in range(6):
        my_str += str(random.randint(0, 9))

    params = dict(code=my_str)
    params = json.dumps(params)
    print celery.send_task('push_srv.create_user_send_sms',
                     args=['17621036594', '木叶苍蓝', 'SMS_109460219', params], queue='sub_push')
