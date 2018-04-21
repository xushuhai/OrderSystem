#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/14 13:29
# @Author  : Xsh
# @File    : base_func.py
# @Software: PyCharmi

import datetime


class BaseFunc(object):
    """ 公共方法 """

    def __init__(self):
        self.create_time = datetime.datetime.now()
        self.update_time = datetime.datetime.now()

    def to_dict(self):
        dictionary = {}
        dictionary.update(self.__dict__)
        if "_sa_instance_state" in dictionary:
            del dictionary['_sa_instance_state']
        return dictionary
