#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/19 15:55
# @Author  : Xsh
# @File    : verifying_code.py
# @Software: PyCharm

import datetime
import hashlib

# from instance.order_app import db
from config.order_app import db
from model.base_func import BaseFunc


class VerifyingCode(BaseFunc, db.Model):
    """ 用户验证码 """
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    telephone = db.Column('telephone', db.String(11))  # 用户手机号码
    verifying_code = db.Column('verifying_code', db.String(6))  # 用户验证码
    create_time = db.Column('create_time', db.TIMESTAMP)  # 创建时间
    update_time = db.Column('update_time', db.TIMESTAMP)  # 更新时间

    def __init__(self, telephone, verifying_code):
        BaseFunc.__init__(self)

        self.telephone = telephone
        self.verifying_code = verifying_code