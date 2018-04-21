#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/15 15:00
# @Author  : Xsh
# @File    : push_srv.py
# @Software: PyCharm

import os, sys

cur_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, cur_path + "/../../")
import traceback
import uuid
import json
from celery import Celery
from log.info import logger
from send_sms.send_sms import send_sms

celery = Celery('tasks')
celery.config_from_object('celeryconfig_msg')


@celery.task
def create_user_send_sms(telephone, sign_name, template_code, template_param=None):
    business_id = uuid.uuid1()
    result = send_sms(business_id, telephone, sign_name, template_code, template_param)
    result = json.loads(result)
    if str(result['Message']) == 'OK':
        logger.info('SMS sending success Message:{}, mobile:{}, param:{} '.format(result['Message'], telephone,
                                                                                           template_param))
    else:
        logger.info('SMS sending failure Message:{}, mobile:{}'.format(result['Message'], telephone))
