#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/24 13:50
# @Author  : Xsh
# @File    : order_v1.py.py
# @Software: PyCharm

from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
