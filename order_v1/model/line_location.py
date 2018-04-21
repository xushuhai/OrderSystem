#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/25 15:32
# @Author  : Xsh
# @File    : line_location.py
# @Software: PyCharm

# from instance.order_app import db
from config.order_app import db
from model.base_func import BaseFunc


class LineLocations(BaseFunc, db.Model):
    """ 线路径停点表 """
    __tablename__ = 'line_location'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    fk_line_code = db.Column('fk_line_code', db.String(256))  # 线路编码
    origin_code = db.Column('origin_code', db.String(6))  # 始发地编码
    destination_code = db.Column('destination_code', db.String(6))  # 目的地编码
    location_code = db.Column('location_code', db.String(6))  # 转运网点编码
    sequence = db.Column('sequence', db.Integer)  # 径停点顺序
    location_status = db.Column('location_status', db.Integer)  # 转运中心属性 1 启用， 2 禁用
    fk_operator_id = db.Column('fk_operator_id', db.Integer)  # 操作人id
    create_time = db.Column('create_time', db.TIMESTAMP)  # 创建时间
    update_time = db.Column('update_time', db.TIMESTAMP)  # 更新时间

    def __init__(self, fk_line_code, origin_code, destination_code, location_code, sequence, location_status,
                 fk_operator_id):
        BaseFunc.__init__(self)

        self.fk_line_code = fk_line_code
        self.origin_code = origin_code
        self.destination_code = destination_code
        self.location_code = location_code
        self.sequence = sequence
        self.location_status = location_status
        self.fk_operator_id = fk_operator_id
