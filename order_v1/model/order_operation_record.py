#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/20 14:37
# @Author  : Xsh
# @File    : order_operation_record.py
# @Software: PyCharm

# from instance.order_app import db
from config.order_app import db
from model.base_func import BaseFunc


class OrderOperationRecord(BaseFunc, db.Model):
    """ 订单操作人记录表 """
    __tablename__ = 'order_operation_record'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    fk_order_number = db.Column('fk_order_number', db.String(24))  # 订单号
    action = db.Column('action', db.Integer)  # 操作类型
    op_time = db.Column('op_time', db.TIMESTAMP)  # 操作时间
    fk_operator_id = db.Column('fk_operator_id', db.Integer)  # 操作人id
    remark = db.Column('remark', db.Text)  # 备注
    create_time = db.Column('create_time', db.TIMESTAMP)  # 创建时间
    update_time = db.Column('update_time', db.TIMESTAMP)  # 更新时间

    def __init__(self, fk_order_number, action, op_time, fk_operator_id, remark):
        BaseFunc.__init__(self)

        self.fk_order_number = fk_order_number
        self.action = action
        self.op_time = op_time
        self.fk_operator_id = fk_operator_id
        self.remark = remark

