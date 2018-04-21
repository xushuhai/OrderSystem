#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/14 14:18
# @Author  : Xsh
# @File    : test.py
# @Software: PyCharm

CONFIG_NAME = "test"

# Redis配置
REDIS_DB = 5
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_PASSWORD = ''
REDIS_URL = 'redis://:%s@%s:%s/%s'%(REDIS_PASSWORD,REDIS_HOST,REDIS_PORT,REDIS_DB)
REDIS_PUB_URL = 'redis://:%s@%s:%s/%s'%(REDIS_PASSWORD,REDIS_HOST,REDIS_PORT,REDIS_DB)

# Database 配置
MY_USER = 'root'
MY_DB = 'order_system'
MY_HOST = '127.0.0.1'
MY_PORT = 3306
MY_PASSWORD = '123456'
SQLALCHEMY_DATABASE_URI = 'mysql://%s:%s@%s:%s/%s?charset=utf8'%(MY_USER,MY_PASSWORD,MY_HOST,MY_PORT,MY_DB)
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_ECHO = True

#  sms Celery redis 配置
REDIS_REQUEST_DB = 6
REDIS_REQUEST_HOST = '127.0.0.1'
REDIS_REQUEST_PORT = 6379
REDIS_REQUEST_PASSWORD = ''
REDIS_URL_REQUEST =  'redis://:%s@%s:%s/%s'%(REDIS_REQUEST_PASSWORD,REDIS_REQUEST_HOST,REDIS_REQUEST_PORT,REDIS_REQUEST_DB)

REDIS_REPONSE_DB = 7
REDIS_REPONSE_HOST = '127.0.0.1'
REDIS_REPONSE_PORT = 6379
REDIS_REPONSE_PASSWORD = ''
REDIS_URL_REPONSE =  'redis://:%s@%s:%s/%s'%(REDIS_REPONSE_PASSWORD,REDIS_REPONSE_HOST,REDIS_REPONSE_PORT,REDIS_REPONSE_DB)

# create user send sms config
SIGN_NAME = '木叶苍蓝'
TEMPLATE_CODE = 'SMS_109460219'
CELERY_ROUTE_CREATE = 'push_srv.create_user_send_sms'
QUEUE = 'sub_push'

# Session config
DAYS = 7

# 不需要token的路由放在这
FILTER_AUTH = ['/order/auth/login','/order/auth/verifying','/order/auth/register','/order/auth/reset_password','/']

# Log 配置
LOG_LEVEL = 'INFO'
LOG_NAME = 'order_app'

# Token 过期
EXPIRE_TIME = 2*3600  # 2h

# sms verifying code expire time
SMS_EXPIRE_TIME = 300

