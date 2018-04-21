#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/25 15:32
# @Author  : Xsh
# @File    : line.py
# @Software: PyCharm

# from instance.order_app import db
from config.order_app import db
from model.base_func import BaseFunc


class Waybill(BaseFunc, db.Model):
    """ 运单表 """
    __tablename__ = 'waybill'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    waybill_number = db.Column('waybill_number', db.String(15))  # 运单号
    waybill_type = db.Column('waybill_type', db.Integer)  # 运单类型 1:正常,2:异常,3:废止
    waybill_status = db.Column('waybill_status', db.Integer)  # 运单状态 200:待装车,300:运输中,500:已完成
    is_onway = db.Column('is_onway', db.Integer)  # 是否在途 1:在途 2:到达
    line_no = db.Column('line_no', db.String(100))  # 线路编号
    fk_to_location_code = db.Column('fk_to_location_code', db.String(8))  # 出发地编码
    fk_at_location_code = db.Column('fk_at_location_code', db.String(8))  # 到达地编码
    plate = db.Column('plate', db.String(8))  # 车牌
    start_time = db.Column('start_time', db.TIMESTAMP)  # 车辆出发时间
    end_time = db.Column('end_time', db.TIMESTAMP)  # 车辆到达时间
    driver_name = db.Column('driver_name', db.String(100))  # 司机姓名
    driver_telephone = db.Column('driver_telephone', db.String(11))  # 司机号码
    remarks = db.Column('remarks', db.Text)  # 备注
    fk_operator_id = db.Column('fk_operator_id', db.Integer)  # 操作人id
    create_date = db.Column('create_date', db.Date)  # 创建日期
    create_time = db.Column('create_time', db.TIMESTAMP)  # 创建时间
    update_time = db.Column('update_time', db.TIMESTAMP)  # 更新时间

    def __init__(self, waybill_number, waybill_type, waybill_status, line_no, fk_to_location_code, fk_at_location_code,
                 plate, start_time, end_time,driver_name, driver_telephone, remarks, fk_operator_id,create_data):
        BaseFunc.__init__(self)

        self.waybill_number = waybill_number
        self.waybill_type = waybill_type
        self.waybill_status = waybill_status
        self.line_no = line_no
        self.fk_to_location_code = fk_to_location_code
        self.fk_at_location_code = fk_at_location_code
        self.plate = plate
        self.start_time = start_time
        self.end_time = end_time
        self.driver_name = driver_name
        self.driver_telephone = driver_telephone
        self.remarks = remarks
        self.fk_operator_id = fk_operator_id
        self.create_date = create_data