#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/20 13:56
# @Author  : Xsh
# @File    : cargo_order.py
# @Software: PyCharm

# from instance.order_app import db
from config.order_app import db
from model.base_func import BaseFunc


class CargoOrder(BaseFunc, db.Model):
    """ 货物订单主表 """
    __tablename__ = 'cargo_order'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    cargo_order_number = db.Column('cargo_order_number', db.String(24))  # 订单号
    fk_waybill_number = db.Column('fk_waybill_number', db.String(15))  # 外键运单号
    fk_line_code = db.Column('fk_line_code', db.String(25))  # 外键线路编号
    origin_code = db.Column('origin_code', db.String(11))  # 始发地编码
    destination_code = db.Column('destination_code', db.String(11))  # 目的地编码
    order_status = db.Column('order_status', db.Integer)  # 订单状态
    order_type = db.Column('order_type', db.String(12))  # 订单类型 整车 零担
    cargo_name = db.Column('cargo_name', db.String(128))  # 货物名称
    cargo_volume = db.Column('cargo_volume', db.String(11))  # 货物体积
    cargo_weight = db.Column('cargo_weight', db.String(8))  # 货物重量
    specified_arrival_time = db.Column('specified_arrival_time', db.TIMESTAMP)  # 规定到达时间
    consignor_name = db.Column('consignor_name', db.String(24))  # 发货人姓名
    consignor_telephone = db.Column('consignor_telephone', db.String(11))  # 发货人联系方式
    consignee_name = db.Column('consignee_name', db.String(24))  # 收货人姓名
    consignee_telephone = db.Column('consignee_telephone', db.String(11))  # 收货人联系方式
    fk_operator_id = db.Column('fk_operator_id', db.Integer)  # 操作人id
    remark = db.Column('remark', db.Text)  # 备注
    create_date = db.Column('create_date', db.Date)  # 创单日期
    create_time = db.Column('create_time', db.TIMESTAMP)  # 创建时间
    update_time = db.Column('update_time', db.TIMESTAMP)  # 更新时间

    def __init__(self, cargo_order_number, origin_code, destination_code, order_status, order_type, cargo_name,
                 cargo_volume,
                 cargo_weight, specified_arrival_time, consignor_name, consignor_telephone, consignee_name,
                 consignee_telephone, fk_operator_id, remark, create_date):
        BaseFunc.__init__(self)

        self.cargo_order_number = cargo_order_number
        self.origin_code = origin_code
        self.destination_code = destination_code
        self.order_status = order_status
        self.order_type = order_type
        self.cargo_name = cargo_name
        self.cargo_volume = cargo_volume
        self.cargo_weight = cargo_weight
        self.specified_arrival_time = specified_arrival_time
        self.consignor_name = consignor_name
        self.consignor_telephone = consignor_telephone
        self.consignee_name = consignee_name
        self.consignee_telephone = consignee_telephone
        self.fk_operator_id = fk_operator_id
        self.remark = remark
        self.create_date = create_date
