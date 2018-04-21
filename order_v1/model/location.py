#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/21 10:54
# @Author  : Xsh
# @File    : location.py
# @Software: PyCharm

# from instance.order_app import db
from config.order_app import db
from model.base_func import BaseFunc


class Location(BaseFunc, db.Model):
    """ 网点信息表 """
    __tablename__ = 'location'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    location_name = db.Column('location_name', db.String(256))  #  网点名称
    location_code = db.Column('location_code', db.Integer)  # 网点编码
    detailed_address = db.Column('detailed_address', db.String(256))  # 网点详细地址
    lot = db.Column('lot', db.Integer)  # 经度
    lat = db.Column('lat', db.Integer)  # 纬度
    province = db.Column('province', db.String(256))  # 省份
    city = db.Column('city', db.String(256))  # 省份
    location_status = db.Column('location_status', db.Integer)  # 转运网点属性 1 启动，2 禁用
    create_time = db.Column('create_time', db.TIMESTAMP)  # 创建时间
    update_time = db.Column('update_time', db.TIMESTAMP)  # 更新时间

    def __init__(self, location_name, location_code, detailed_address, lot, lat, province, city, location_status):
        BaseFunc.__init__(self)

        self.location_name = location_name
        self.location_code = location_code
        self.detailed_address = detailed_address
        self.lot = lot
        self.lat = lat
        self.province = province
        self.city = city
        self.location_status = location_status