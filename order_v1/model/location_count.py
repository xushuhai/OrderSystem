#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/27 21:49
# @Author  : Xsh
# @File    : location_count.py
# @Software: PyCharm


# from instance.order_app import db
from config.order_app import db
from model.base_func import BaseFunc



class LocationCount(BaseFunc, db.Model):
    """ 订单号生成表 """
    __tablename__ = 'location_count'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    location_amount = db.Column('location_amount', db.Integer)   # 总数
    create_time = db.Column('create_time', db.TIMESTAMP)   # 创建时间
    update_time = db.Column('update_time', db.TIMESTAMP)   # 更新时间

    def __init__(self, location_amount):
        BaseFunc.__init__(self)

        self.location_amount = location_amount