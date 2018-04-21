#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/8 11:12
# @Author  : Xsh
# @File    : waybill.py
# @Software: PyCharm

import traceback
from datetime import date

from config.order_app import db
from model.waybill import Waybill
from model.line import Line
from model.truck import Truck
from model.cargo_order import CargoOrder

from service.order import generate_order_number
from service.line_volume import line_volume_get
from tools import constant as cs
from cache.helper import hgetall
from cache.keys import get_token
from log.info import logger


def create_waybill(token, line_code, start_time, end_time, plate, driver_name, driver_telephone, remarks,
                   cargo_order_numbers):
    """
    创建运单
    :param token:
    :param line_code:  线路编号
    :param start_time:  发车时间
    :param end_time:  到车时间
    :param plate:  车牌
    :param driver_name:  司机姓名
    :param driver_telephone:  司机号码
    :param remarks:  备注
    :param cargo_order_numbers:  货物订单号集合
    :return: 1000, 运单号
    """
    try:
        user = hgetall(get_token(token))
        if (not user) or int(user['role_type']) != cs.USER_ROLE_INFO[u"运单统筹专员"]:
            return cs.AUTH_ERROR, None
        # 验证线路
        line_obj = Line.query.filter_by(line_code=line_code).first()
        if not line_obj:
            return cs.LINE_CODE_ERR, None
        # 验证车牌
        truck_obj = Truck.query.filter_by(plate=plate).first()
        if not truck_obj:
            return cs.PLATE_ERR, None

        # 生成运单号
        waybill_number = 'W' + generate_order_number(date.today(), cs.ORDER_INFO[u"运输订单"])
        # 获取始发地编码
        fk_to_location_code = line_obj.origin_code
        # 获取目的地编码
        fk_at_location_code = line_obj.destination_code
        # 初始化运单
        waybill = Waybill(waybill_number, cs.WAYBILL_TYPE_INFO[u"正常"], cs.WAYBILL_STATUS_INFO[u"待装车"], line_code,
                          fk_to_location_code, fk_at_location_code, plate, start_time, end_time, driver_name,
                          driver_telephone, remarks, user['id'], date.today())

        if cargo_order_numbers:
            cargos_volume = 0
            cargos_weight = 0
            for cargo_order_number in cargo_order_numbers:
                cargo_order_obj = CargoOrder.query.filter_by(cargo_order_number=cargo_order_number).first()
                if not cargo_order_obj:
                    return cs.NOT_CARGO_ORDER, {'err_cargo_order_number': cargo_order_number}
                if cargo_order_obj.order_status != cs.CARGO_ORDER_STATUS_INFO[u"待接单"]:
                    print cargo_order_obj.order_status
                    print cs.CARGO_ORDER_STATUS_INFO[u"待接单"]
                    return cs.CARGO_ORDER_STATUS_ABNORMAL, {'err_cargo_order_number': cargo_order_number}

                # 更新货物订单
                cargo_order_obj.order_status = cs.CARGO_ORDER_STATUS_INFO[u"已接单"]
                cargo_order_obj.fk_waybill_number = waybill_number
                # 统计
                cargos_volume += cargo_order_obj.cargo_volume
                cargos_weight += cargo_order_obj.cargo_weight
            # 修改line_volume
            err, result = line_volume_get(line_code, cargos_volume, cargos_weight, user['id'])
            if err:
                return err, result

        db.session.add(waybill)
        db.session.commit()
        return cs.OK, {'waybill_number': waybill_number}
    except:
        logger.error('create_waybill err:{}'.format(traceback.format_exc(), ))
        raise
    finally:
        db.session.rollback()


def modify_waybill(token, waybill_number, plate, driver_name, driver_telephone, start_time, end_time,
                   cargo_order_numbers, remarks):
    """
    修改运单数据
    :param token:
    :param waybill_number: 运单号
    :param plate: 车牌
    :param driver_name: 司机姓名
    :param driver_telephone: 司机号码
    :param start_time: 发车时间
    :param end_time: 到车时间
    :param cargo_order_numbers: 订单号集合
    :param remarks: 备注
    :return: 1000, 运单号
    """
    try:
        user = hgetall(get_token(token))
        if (not user) or int(user['role_type']) != cs.USER_ROLE_INFO[u"运单统筹专员"]:
            return cs.AUTH_ERROR, None
        # 验证运单
        waybill_obj = Waybill.query.filter_by(waybill_number=waybill_number).first()
        if not waybill_obj:
            return cs.WAYBILL_NUMBER_ERR, {"err_waybill_number": waybill_number}
        if waybill_obj.waybill_status != cs.WAYBILL_STATUS_INFO[u"待装车"]:
            return cs.WAYBILL_STATUS_ERR, {"err_waybill_number": waybill_number}

        # 验证车牌
        truck_obj = Truck.query.filter_by(plate=plate).first()
        if not truck_obj:
            return cs.PLATE_ERR, None
        # 修改运单数据
        waybill_obj.plate = plate
        waybill_obj.driver_name = driver_name
        waybill_obj.driver_telephone = driver_telephone
        waybill_obj.start_time = start_time
        waybill_obj.end_time = end_time

        # 释放绑定的货物订单
        cargo_order_objs = CargoOrder.query.filter_by(fk_waybill_number=waybill_number).all()
        if cargo_order_objs:
            for cargo_order_obj in cargo_order_objs:
                cargo_order_obj.order_status = cs.CARGO_ORDER_STATUS_INFO[u"待接单"]
                cargo_order_obj.fk_waybill_number = None
        # 重新绑定货物订单
        if cargo_order_numbers:
            for cargo_order_number in cargo_order_numbers:
                cargo_order_obj = CargoOrder.query.filter_by(cargo_order_number=cargo_order_number).first()
                if not cargo_order_obj:
                    return cs.NOT_CARGO_ORDER, {'err_cargo_order_number': cargo_order_number}
                if cargo_order_obj.order_status != cs.CARGO_ORDER_STATUS_INFO[u"待接单"]:
                    return cs.CARGO_ORDER_STATUS_ABNORMAL, {'err_cargo_order_number': cargo_order_number}
                # 更新货物订单
                cargo_order_obj.order_status = cs.CARGO_ORDER_STATUS_INFO[u"已接单"]
                cargo_order_obj.fk_waybill_number = waybill_number
        db.session.commit()
        return cs.OK, {'waybill_number': waybill_number}
    except:
        logger.error('create_waybill err:{}'.format(traceback.format_exc(), ))
        raise
    finally:
        db.session.rollback()


def modify_waybill_status(token, waybill_number, waybill_status):
    """
    修改运单状态
    :param token:
    :param waybill_number: 运单号
    :param waybill_status: 运单状态 200:待装车, 300:运输中 , 500:已完成
    :return:1000, 运单号
    """
    try:
        user = hgetall(get_token(token))
        if (not user) or int(user['role_type']) != cs.USER_ROLE_INFO[u"运单统筹专员"]:
            return cs.AUTH_ERROR, None
        # user['fk_location_code'] = int(user['fk_location_code'])
        # 验证运单
        waybill_obj = Waybill.query.filter_by(waybill_number=waybill_number).first()
        if not waybill_obj:
            return cs.WAYBILL_NUMBER_ERR, {"err_waybill_number": waybill_number}
        # 对运单状态进行验证
        if waybill_status != cs.WAYBILL_STATUS_CHANGE[waybill_obj.waybill_status]:
            return cs.WAYBILL_STATUS_ERR, {'err_waybill_number': waybill_number}
        # 验证运单修改状态与用户权限是否匹配
        if waybill_status == cs.WAYBILL_STATUS_INFO[u"运输中"]:
            if user['fk_location_code'] != waybill_obj.fk_to_location_code:
                return cs.AUTH_ERROR, None
        if waybill_status == cs.WAYBILL_STATUS_INFO[u"已完成"]:
            if user['fk_location_code'] != waybill_obj.fk_at_location_code:
                return cs.AUTH_ERROR, None

        waybill_obj.waybill_status = waybill_status
        # 修改关联货物订单状态
        # 根据运单号查询对应的货物订单
        cargo_order_objs = CargoOrder.query.filter_by(fk_waybill_number=waybill_number).all()
        if cargo_order_objs:
            for cargo_order_obj in cargo_order_objs:
                cargo_order_obj.order_status = cs.WAYBILL_CARGO_STATUS_CHANGE[waybill_status]

        db.session.commit()
        return cs.OK, {'waybill_number': waybill_number}
    except:
        logger.error('create_waybill err:{}'.format(traceback.format_exc(), ))
        raise
    finally:
        db.session.rollback()


def modify_waybill_type(token, waybill_number, waybill_type, remarks):
    """
    修改运单属性
    :param token:
    :param waybill_numberm:
    :param waybill_type: 运单类型: 1:正常, 2:异常, 3:废止
    :return: 1000, 运单号
    """
    try:
        user = hgetall(get_token(token))
        if (not user) or int(user['role_type']) != cs.USER_ROLE_INFO[u"运单统筹专员"]:
            return cs.AUTH_ERROR, None
        # 验证运单
        waybill_obj = Waybill.query.filter_by(waybill_number=waybill_number).first()
        if not waybill_obj:
            return cs.WAYBILL_NUMBER_ERR, {"err_waybill_number": waybill_number}
        # 修改关联货物订单类型，同时增加备注
        # 根据运单号查询对应的货物订单
        if waybill_obj.waybill_status == cs.WAYBILL_STATUS_INFO[u"待装车"]:
            if waybill_type == cs.WAYBILL_TYPE_INFO[u'废止']:
                # 修改运单属性
                waybill_obj.waybill_type = waybill_type
                waybill_obj.remarks = remarks
                # 释放订单
                cargo_order_objs = CargoOrder.query.filter_by(fk_waybill_number=waybill_number).all()
                if cargo_order_objs:
                    for cargo_order_obj in cargo_order_objs:
                        cargo_order_obj.order_status = cs.CARGO_ORDER_STATUS_INFO[u"待接单"]
                        cargo_order_obj.fk_waybill_number = None
            else:
                waybill_obj.waybill_type = waybill_type
                waybill_obj.remarks = remarks

        elif waybill_obj.waybill_status == cs.WAYBILL_STATUS_INFO[u"运输中"]:
            # 修改运单属性
            waybill_obj.waybill_type = waybill_type
            waybill_obj.remarks = remarks
            # 修改订单属性
            cargo_order_objs = CargoOrder.query.filter_by(fk_waybill_number=waybill_number).all()
            if cargo_order_objs:
                for cargo_order_obj in cargo_order_objs:
                    cargo_order_obj.order_status = cs.WAYBILL_TYPE_ORDER_STATUS[waybill_type]
                    if waybill_type == cs.WAYBILL_TYPE_INFO[u"废止"]:
                        cargo_order_obj.fk_waybill_number = None
        db.session.commit()
        return cs.OK, {'waybill_number': waybill_number}
    except:
        logger.error('create_waybill err:{}'.format(traceback.format_exc(), ))
        raise
    finally:
        db.session.rollback()
