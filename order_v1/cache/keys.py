#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/19 16:50
# @Author  : Xsh
# @File    : keys.py
# @Software: PyCharm


def get_token(key):
    return 'token:{}'.format(key)


def get_sms(key):
    return 'sms:{}'.format(key)


def push_line(key):
    return 'PushLine:{}'.format(key)