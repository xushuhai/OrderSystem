#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/3 15:27
# @Author  : Xsh
# @File    : truck.py
# @Software: PyCharm


# from instance.order_app import db
from config.order_app import db
from model.base_func import BaseFunc


class Truck(BaseFunc, db.Model):
    """ 车辆表 """
    __tablename__ = 'truck'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    plate = db.Column('plate', db.String(256))  # 车牌
    status = db.Column('status', db.Integer)  # 车辆状态 1启用，2禁用
    container_type = db.Column('container_type', db.Integer)  # 车厢类型 1箱式，2高栏
    plate_type = db.Column('plate_type', db.Integer)  # 车牌类型 1一般货车,2挂车,3车厢'
    vehicle_type = db.Column('vehicle_type', db.Integer)  # 车辆类型 1临时，2正式
    container_length = db.Column('container_length', db.String(10))  # 车厢长度
    container_wide = db.Column('container_wide', db.String(10))  # 车厢宽度
    container_high = db.Column('container_high', db.String(10))  # 车厢高度
    container_volume = db.Column('container_volume', db.String(10))  # 车厢体积
    fk_operator_id = db.Column('fk_operator_id', db.Integer)  # 操作人id
    create_time = db.Column('create_time', db.TIMESTAMP)  # 创建时间
    update_time = db.Column('update_time', db.TIMESTAMP)  # 更新时间

    def __init__(self, plate, status, plate_type, vehicle_type, container_type, container_length,
                 container_wide,
                 container_high, container_volume, fk_operator_id):
        BaseFunc.__init__(self)

        self.plate = plate
        self.status = status
        self.container_type = container_type
        self.plate_type = plate_type
        self.vehicle_type = vehicle_type
        self.container_length = container_length
        self.container_wide = container_wide
        self.container_high = container_high
        self.container_volume = container_volume
        self.fk_operator_id = fk_operator_id
