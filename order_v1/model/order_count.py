#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/20 14:18
# @Author  : Xsh
# @File    : order_count.py
# @Software: PyCharm

# from instance.order_app import db
from config.order_app import db
from model.base_func import BaseFunc


class OrderCount(BaseFunc, db.Model):
    """ 订单号生成表 """
    __tablename__ = 'order_count'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    order_date = db.Column('order_date', db.Date)          # 日期
    order_amount = db.Column('order_amount', db.Integer)   # 总数
    order_type = db.Column('order_type', db.Integer)       # 订单类型
    create_time = db.Column('create_time', db.TIMESTAMP)   # 创建时间
    update_time = db.Column('update_time', db.TIMESTAMP)   # 更新时间

    def __init__(self, order_date, order_amount, order_type):
        BaseFunc.__init__(self)

        self.order_date = order_date
        self.order_amount = order_amount
        self.order_type = order_type


