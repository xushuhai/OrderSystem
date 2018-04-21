#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/22 14:26
# @Author  : Xsh
# @File    : order.py
# @Software: PyCharm

import json
from datetime import datetime
from config.order_app import db
from cache.helper import rset
from cache.keys import push_line
from model.order_flow import OrderFlow
from model.order_count import OrderCount
from model.order_operation_record import OrderOperationRecord as ooRecord
from model.line_location import LineLocations

from service.auth import get_user_username
from tools import constant as cs


def get_order_flows(fk_order_number):
    """
    获取订单流记录
    :param fk_order_number:
    :return: list
    """
    order_flows = []
    order_flow_objs = OrderFlow.query.filter_by(fk_order_number=fk_order_number).all()
    for item in order_flow_objs:
        order_flows.append(item.order_status)
    return order_flows


def get_operation_records(order_number, action=None):
    """
    获取订单操作记录流
    :param order_number:
    :param action:
    :return: list
    """
    if action:
        ooRecord_obj = ooRecord.query.filter_by(fk_order_number=order_number, action=action).first()
        return ooRecord_obj
    else:
        ooRecord_objs = ooRecord.query.filter_by(fk_order_number=order_number).all()
        operation_records = []
        for item in ooRecord_objs:
            op_time = item.op_time
            action = cs.CARGO_ORDER_STATUS_INDEX[item.action]
            action_description = cs.ACTION_TYPE_INDEX[item.action]
            remark = item.remark
            operator_name = get_user_username(item.fk_operator_id)
            operation_records.append(
                dict(op_time=op_time, action=action, action_description=action_description, remark=remark,
                     operator_name=operator_name))
        return operation_records


def generate_order_number(date_value, order_type):
    """
    生成订单号
    :param date_value:
    :param order_type:
    :return:string
    """
    order_count_obj = OrderCount.query.filter_by(order_date=date_value, order_type=order_type).first()
    if order_count_obj:
        order_amount = order_count_obj.order_amount + 1
        order_count_obj.order_amount = order_amount
        order_count_obj.update_time = datetime.now()
    else:
        order_amount = 1
        order_count_new = OrderCount(date_value, order_amount, order_type)
        db.session.add(order_count_new)
        db.session.commit()
    amounter = str(order_amount).zfill(5)
    date_string = date_value.strftime('%Y%m%d')
    return '{}{}'.format(date_string, amounter)


def push_line_info(cargo_order_number, origin_code, destination_code):
    """
    推送线路信息
    :param cargo_order_number:  订单号
    :return: None
    """
    line_no_list = []
    line_locations = LineLocations.query.filter_by(location_code=origin_code).all()
    for item in line_locations:
        line_location = LineLocations.query.filter_by(fk_line_code=item.fk_line_code,
                                                      location_status=cs.LINE_LOCATION_STATUS_INFO[u"启用"],
                                                      location_code=destination_code).filter(
            'line_location.sequence > %s' % item.sequence).first()
        if line_location:
            line_no_list.append(line_location.fk_line_code)
    rset(push_line(cargo_order_number), json.dumps(line_no_list))
