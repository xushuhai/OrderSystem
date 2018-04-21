#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/18 15:55
# @Author  : Xsh
# @File    : wsgi.py
# @Software: PyCharm

from manage import app as application

if __name__ == "__main__":
    application.run()
