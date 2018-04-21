#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/14 13:23
# @Author  : Xsh
# @File    : user.py
# @Software: PyCharm

import datetime
import hashlib

# from instance.order_app import db
from config.order_app import db
from model.base_func import BaseFunc


class User(BaseFunc, db.Model):
    """ 用户 """
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column('name', db.String(32))  # 用户名
    username = db.Column('username', db.String(11))  # 登录帐号
    password = db.Column('password', db.String(256), nullable=False)  # 登录密码
    mobile = db.Column('mobile', db.String(11))  # 用户手机号码
    role_type = db.Column('role_type', db.Integer)  # 用户类型
    fk_location_code = db.Column('fk_location_code', db.String(6))  # 用户所属转运网点
    fk_plate = db.Column('fk_plate', db.String(11))  # 车牌
    create_time = db.Column('create_time', db.TIMESTAMP)  # 创建时间
    update_time = db.Column('update_time', db.TIMESTAMP)  # 更新时间

    def __init__(self, name, username, password, mobile, role_type, fk_location_code, fk_plate):
        BaseFunc.__init__(self)
        self.name = name
        self.username = username
        self.password = password
        self.mobile = mobile
        self.role_type = role_type
        self.fk_location_code = fk_location_code
        self.fk_plate = fk_plate

