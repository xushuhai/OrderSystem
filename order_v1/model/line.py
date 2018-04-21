#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/25 15:32
# @Author  : Xsh
# @File    : line.py
# @Software: PyCharm

# from instance.order_app import db
from config.order_app import db
from model.base_func import BaseFunc


class Line(BaseFunc, db.Model):
    """ 线路表 """
    __tablename__ = 'line'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    line_code = db.Column('line_code', db.String(256))  # 线路编码
    line_name = db.Column('line_name', db.String(256))  # 线路名称
    origin_code = db.Column('origin_code', db.String(6))  # 始发地编码
    destination_code = db.Column('destination_code', db.String(6))  # 目的地编码
    line_status = db.Column('line_status', db.Integer)  # 线路状态 1 启用，2 禁用
    line_type = db.Column('line_type', db.Integer)  # 线路属性 1 临时， 2 正式
    line_kilometre = db.Column('line_kilometre', db.Integer)  # 线路运行公里数
    line_runtime = db.Column('line_runtime', db.String(256))  # 线路运行时长
    location_number = db.Column('location_number')  # 径停点数量
    fk_operator_id = db.Column('fk_operator_id', db.Integer)  # 操作人id
    create_time = db.Column('create_time', db.TIMESTAMP)  # 创建时间
    update_time = db.Column('update_time', db.TIMESTAMP)  # 更新时间

    def __init__(self, line_code, line_name, origin_code, destination_code, line_status, line_type, line_kilometre,
                 line_runtime, location_number, fk_operator_id):
        BaseFunc.__init__(self)

        self.line_code = line_code
        self.line_name = line_name
        self.origin_code = origin_code
        self.destination_code = destination_code
        self.line_status = line_status
        self.line_type = line_type
        self.line_kilometre = line_kilometre
        self.line_runtime = line_runtime
        self.location_number = location_number
        self.fk_operator_id = fk_operator_id
