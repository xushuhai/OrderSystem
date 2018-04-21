#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/20 14:31
# @Author  : Xsh
# @File    : order_flow.py
# @Software: PyCharm

# from instance.order_app import db
from config.order_app import db
from model.base_func import BaseFunc


class OrderFlow(BaseFunc, db.Model):
    """ 订单状态流表 """
    __tablename__ = 'order_flow'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    fk_order_number = db.Column('fk_order_number', db.String(24))  # 订单号
    order_status = db.Column('order_status', db.Integer)  # 订单状态
    status_time = db.Column('status_time', db.TIMESTAMP)  # 状态时间
    remark = db.Column('remark', db.Text)  # 备注
    fk_operator_id = db.Column('fk_operator_id', db.Integer)  # 操作者id
    create_time = db.Column('create_time', db.TIMESTAMP)  # 创建时间
    update_time = db.Column('update_time', db.TIMESTAMP)  # 更新时间

    def __init__(self, fk_order_number, order_status, status_time,remark,fk_operator_id):
        BaseFunc.__init__(self)

        self.fk_order_number = fk_order_number
        self.order_status = order_status
        self.status_time = status_time
        self.remark = remark
        self.fk_operator_id = fk_operator_id
