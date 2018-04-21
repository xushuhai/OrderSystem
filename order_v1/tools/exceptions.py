#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/18 10:05
# @Author  : Xsh
# @File    : exceptions.py
# @Software: PyCharm

from log.info import logger


class ParamError(IOError):

    def __init__(self, value=''):
        self.value = value
        super(ParamError, self).__init__(value)
        logger.warning("ParamError:{value}".format(value=str(value)))

    def __str__(self):
        return repr(self.value)


class AuthError(Exception):

    def __init__(self, value=''):
        self.value = value
        logger.error("AuthError:{value}".format(value=str(value)))

    def __str__(self):
        return repr(self.value)