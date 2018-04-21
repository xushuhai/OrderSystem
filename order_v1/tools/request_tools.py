#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/18 09:57
# @Author  : Xsh
# @File    : request_tools.py
# @Software: PyCharm

from flask import request


def request_data():
    """ Wrap the flask request, return a dict"""
    if request.method in ('POST', "PUT"):
        return request.get_json(force=True)
    else:
        return request.values