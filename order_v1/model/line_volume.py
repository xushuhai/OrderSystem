#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/16 16:06
# @Author  : Xsh
# @File    : line_volume.py
# @Software: PyCharm

# from instance.order_app import db
from config.order_app import db
from model.base_func import BaseFunc


class LineVolume(BaseFunc, db.Model):
    """ 线路货物总数表 """
    __tablename__ = 'line_volume'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    line_code = db.Column('line_code', db.String(256))  # 线路编码
    pending_volume = db.Column('pending_volume', db.Integer)  # 待处理货物方位
    pending_weight = db.Column('pending_weight', db.Integer)  # 待处理货物重量
    processed_volume = db.Column('processed_volume', db.Integer)  # 已处理货物方位
    processed_weight = db.Column('processed_weight', db.Integer)  # 已处理货物重量
    fk_operator_id = db.Column('fk_operator_id', db.Integer)  # 操作人id
    create_time = db.Column('create_time', db.TIMESTAMP)  # 创建时间
    update_time = db.Column('update_time', db.TIMESTAMP)  # 更新时间

    def __init__(self, line_code,pending_volume, pending_weight, fk_operator_id):
        BaseFunc.__init__(self)

        self.line_code = line_code
        self.pending_volume = pending_volume
        self.pending_weight = pending_weight
        self.fk_operator_id = fk_operator_id
