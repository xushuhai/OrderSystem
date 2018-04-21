#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/22 14:03
# @Author  : Xsh
# @File    : cargo_order.py
# @Software: PyCharm


import traceback
import json
from datetime import date
from datetime import datetime

from log.info import logger
from config.order_app import db
from cache.helper import hgetall, rget, delete
from cache.keys import get_token, push_line
from tools import constant as cs
from location import get_location
from model.order_operation_record import OrderOperationRecord as ooRecord
from model.order_flow import OrderFlow
from model.cargo_order import CargoOrder
from model.line import Line
from order import generate_order_number, get_order_flows, get_operation_records, push_line_info
from line_volume import line_volume_set


def create_cargo_order(token, origin_code, destination_code, cargo_name, cargo_volume, cargo_weight,
                       specified_arrival_time, consignor_name, consignor_telephone, consignee_name,
                       consignee_telephone):
    """
    创建货物订单
    :param token:
    :param origin_code:
    :param destination_code:
    :param cargo_name:
    :param cargo_volume:
    :param cargo_weight:
    :param specified_arrival_time:
    :param consignor_name:
    :param consignor_telephone:
    :param consignee_name:
    :param consignee_telephone:
    :return: cs.OK, cargo_order_number
    """
    user = hgetall(get_token(token))
    # 验证用户权限
    if (not user) or int(user['role_type']) != cs.USER_ROLE_INFO[u"货物订单统筹专员"]:
        return cs.AUTH_ERROR, None
    # 验证转运网点
    origin_location = get_location(origin_code)
    destination_location = get_location(destination_code)
    if not origin_location and not destination_location:
        return cs.LOCATION_ERR, None
    if not (origin_location and destination_location):
        return cs.LOCATION_ERR, None
    # 获取货物订单号
    cargo_order_number = 'C' + generate_order_number(date.today(), cs.ORDER_INFO[u"货物订单"])
    now_time = datetime.now()
    order_status = cs.CARGO_ORDER_STATUS_INFO[u"待接单"]
    order_type = cs.ORDER_INFO[u"货物订单"]
    fk_operator_id = user['id']
    remark = None
    try:
        cargo_order = CargoOrder(cargo_order_number, origin_code, destination_code, order_status, order_type,
                                 cargo_name,
                                 cargo_volume, cargo_weight,
                                 specified_arrival_time, consignor_name, consignor_telephone, consignee_name,
                                 consignee_telephone, fk_operator_id, remark, date.today())
        db.session.add(cargo_order)
        remark = None
        oflow_obj = OrderFlow(cargo_order_number, order_status, now_time, remark, fk_operator_id)
        db.session.add(oflow_obj)
        oorecord_obj = ooRecord(cargo_order_number, cs.ACTION_TYPE_INFO[u"创建货物订单"], now_time,
                                fk_operator_id,
                                remark)
        db.session.add(oorecord_obj)
        db.session.commit()
        # 推送线路信息
        push_line_info(cargo_order_number, origin_code, destination_code)
        return cs.OK, cargo_order_number
    except:
        logger.error('create cargo order error: {}'.format(traceback.format_exc(), ))
        raise
    finally:
        db.session.rollback()


def get_cargo_orders(token, start_date, end_date, order_status, cargo_order_number, origin_code,
                     destination_code, page_index, page_size, select_flag):
    """
    获取货物订单列表
    :param token:
    :param start_date:
    :param end_date:
    :param order_status:
    :param cargo_order_number:
    :param origin_code:
    :param destination_code:
    :param page_index:
    :param page_size:
    :param select_flag:
    :return: cs.OK, {}
    """
    user = hgetall(get_token(token))
    user_role_type = int(user['role_type'])
    # 验证用户权限
    if (not user) or int(user['role_type']) not in [cs.USER_ROLE_INFO[u"商家"], cs.USER_ROLE_INFO[u"货物订单统筹专员"]]:
        return cs.AUTH_ERROR, None

    statment = '1=1'

    if True != cs.is_date(start_date) or True != cs.is_date(end_date):
        return cs.PARAMS_ERROR, {'start_date': start_date, 'end_date': end_date}
    else:
        start_date = datetime.strptime(str(start_date), "%Y-%m-%d").date()
        end_date = datetime.strptime(str(end_date), "%Y-%m-%d").date()
        date_interval = (end_date - start_date).days
        if date_interval > 90:
            return cs.DATE_INTERVAL_TOO_LONG, {'date_interval': date_interval}

        statment += " and (cargo_order.create_date between '%s' and '%s')" % (start_date, end_date)

    if cargo_order_number:
        statment = "1=1 and (cargo_order.cargo_order_number = '%s')" % cargo_order_number
    if order_status:
        statment += " and (cargo_order.order_status = '%s')" % order_status
    if user_role_type == cs.USER_ROLE_INFO[u"商家"]:
        statment += " and (cargo_order.fk_operator_id = '%s')" % user['id']
        if destination_code:
            statment += " and (cargo_order.destination_code = '%s')" % destination_code
        if origin_code:
            statment += " and (cargo_order.origin_code = '%s')" % origin_code

    if user_role_type == cs.USER_ROLE_INFO[u"货物订单统筹专员"]:
        if int(select_flag) == cs.SELECT_FLAG_INFO[u"查询始发地订单"]:
            statment += " and (cargo_order.origin_code = '%s')" % user['fk_location_code']
            if destination_code:
                statment += " and (cargo_order.destination_code = '%s')" % destination_code

        if int(select_flag) == cs.SELECT_FLAG_INFO[u"查询目的地订单"]:
            statment += " and (cargo_order.destination_code = '%s')" % user['fk_location_code']
            if origin_code:
                statment += " and (cargo_order.origin_code = '%s')" % origin_code

    cargo_orders = []
    cargo_orders_count = 0
    cargo_orders_objs = CargoOrder.query.filter(statment).order_by(CargoOrder.update_time.desc()).paginate(
        int(page_index),
        int(page_size), False)
    logger.info('get_cargo_orders statment is {}'.format(statment, ))
    cargo_orders_count = db.session.query(CargoOrder.id).filter(statment).count()

    for item in cargo_orders_objs.items:
        cargo_order = {}
        cargo_order['update_time'] = item.update_time
        cargo_order['create_date'] = item.create_date
        cargo_order['order_number'] = item.cargo_order_number
        cargo_order['order_status'] = item.order_status
        cargo_order['cargo_name'] = item.cargo_name
        cargo_order['origin_name'] = get_location(item.origin_code).location_name
        cargo_order['destination_code'] = get_location(item.destination_code).location_name
        cargo_orders.append(cargo_order)
    return cs.OK, {'cargo_orders': cargo_orders, 'orders_count': cargo_orders_count}


def modify_order_status(token, cargo_order_number, cargo_order_status, remark):
    """
    修改货物订单状态
    :param token:
    :param cargo_order_number:
    :param cargo_order_status:
    :param remark:
    :return: cs.OK , {}
    """
    try:
        user = hgetall(get_token(token))
        # 验证用户权限
        if (not user) or int(user['role_type']) not in cs.ACTION_CARGO_ORDER_ROLE:
            return cs.AUTH_ERROR, None

        cargo_order_obj = CargoOrder.query.filter_by(cargo_order_number=cargo_order_number).first()
        if not cargo_order_obj:
            return cs.NOT_CARGO_ORDER, None

        # 验证单号是否属于该商家
        if int(user['role_type']) == cs.USER_ROLE_INFO[u"商家"]:
            if cargo_order_obj:
                if cargo_order_obj.fk_operator_id != user['id']:
                    return cs.AUTH_ERROR, None
            else:
                return cs.NOT_CARGO_ORDER, {'cargo_order_number': cargo_order_number}
        else:
            # 验证订单的始发地，目的地是否属于转运网点
            if user['fk_location_code'] not in [cargo_order_obj.origin_code, cargo_order_obj.destination_code]:
                return cs.AUTH_ERROR, None
        cargo_order_status = int(cargo_order_status)
        # 验证用户操作与权限是否匹配
        if cargo_order_status not in cs.USER_ROLE_ACTION[int(user['role_type'])]:
            return cs.AUTH_ERROR, {'cargo_order_number': cargo_order_number}

        old_cargo_order_status = cargo_order_obj.order_status
        # 验证订单状态
        if cargo_order_status not in cs.CARGO_ORDER_STATUS_CHANGE[int(old_cargo_order_status)]:
            return cs.CARGO_ORDER_STATUS_ABNORMAL, {'cargo_order_number': cargo_order_number}
        cargo_order_obj.order_status = cargo_order_status
        cargo_order_obj.remark = remark

        now_time = datetime.now()
        fk_operator_id = user['id']
        # 添加订单流记录
        oflow_obj = OrderFlow(cargo_order_number, cargo_order_status, now_time, remark, fk_operator_id)
        # 添加操作人记录
        print cs.ACTION_TYPE_INDEX[cargo_order_status]
        action = cs.ACTION_TYPE_INFO[cs.ACTION_TYPE_INDEX[cargo_order_status]]
        oorecord_obj = ooRecord(cargo_order_number, action, now_time,
                                fk_operator_id,
                                remark)
        db.session.add(oorecord_obj)
        db.session.add(oflow_obj)
        db.session.commit()
        return cs.OK, {'cargo_order_number': cargo_order_number}
    except:
        logger.error('cancellation_cargo_order {}'.format(traceback.format_exc(), ))
        raise
    finally:
        db.session.rollback()


def get_cargo_order(token, cargo_order_number):
    """
    查看货物订单详情

    :param token:
    :param cargo_order_number:
    :return: cs.OK, object
    """
    user = hgetall(get_token(token))
    if not user:
        return cs.AUTH_ERROR, None

    # 货物订单信息
    cargo_order_obj = CargoOrder.query.filter_by(cargo_order_number=cargo_order_number).first()
    if not cargo_order_obj:
        return cs.NOT_CARGO_ORDER, None
    cargo_order = {}
    cargo_order['cargo_order_number'] = cargo_order_obj.cargo_order_number
    cargo_order['origin_name'] = get_location(cargo_order_obj.origin_code).location_name
    cargo_order['destination_name'] = get_location(cargo_order_obj.destination_code).location_name
    cargo_order['order_status'] = cargo_order_obj.order_status
    cargo_order['order_type'] = cargo_order_obj.order_type
    cargo_order['cargo_name'] = cargo_order_obj.cargo_name
    cargo_order['cargo_volume'] = cargo_order_obj.cargo_volume
    cargo_order['cargo_weight'] = cargo_order_obj.cargo_weight
    cargo_order['specified_arrival_time'] = cargo_order_obj.specified_arrival_time
    cargo_order['consignor_name'] = cargo_order_obj.consignor_name
    cargo_order['consignor_telephone'] = cargo_order_obj.consignor_telephone
    cargo_order['consignee_name'] = cargo_order_obj.consignee_name
    cargo_order['consignee_telephone'] = cargo_order_obj.consignee_telephone
    cargo_order['create_time'] = cargo_order_obj.create_time
    # 货物订单流
    cargo_order['order_flows'] = get_order_flows(cargo_order_number)
    # 货物订单操作日志
    cargo_order['order_operations'] = get_operation_records(cargo_order_number)
    # 推送线路信息
    line_nos = json.loads(rget(push_line(cargo_order_number)))
    line_list = []
    for line_no in line_nos:
        line_obj = Line.query.filter_by(line_code=line_no, line_status=cs.LINE_STATUS_INFO[u"启用"]).first()
        line_dict = {}
        if line_obj:
            line_dict['line_code'] = line_obj.line_code
            line_dict['line_name'] = line_obj.line_name
            line_dict['line_kilometre'] = line_obj.line_kilometre
            line_dict['line_runtime'] = line_obj.line_runtime
            line_list.append(line_dict)
    cargo_order['push_lines'] = line_list
    # cargo_order['push_lines'] = rget(push_line(cargo_order_number))
    return cs.OK, cargo_order


def cargo_choose_line(token, cargo_order_number, line_code):
    """
    货物订单选择线路
    :param token:
    :param cargo_order_number:  货物订单号
    :param line_code:   线路编号
    :return: cs.OK
    """
    try:
        user = hgetall(get_token(token))
        # 验证用户权限
        if (not user) or int(user['role_type']) != cs.USER_ROLE_INFO[u"货物订单统筹专员"]:
            return cs.AUTH_ERROR, None
        # 验证货物订单
        cargo_order_obj = CargoOrder.query.filter_by(cargo_order_number=cargo_order_number).first()
        if not cargo_order_obj:
            return cs.NOT_CARGO_ORDER, None
        if cargo_order_obj.order_status != cs.CARGO_ORDER_STATUS_INFO[u"待接单"]:
            return cs.CARGO_ORDER_STATUS_ABNORMAL, None
        # 验证线路
        line_obj = Line.query.filter_by(line_code=line_code).first()
        if not line_obj:
            return cs.LINE_CODE_ERR, None
        if line_obj.line_status != cs.LINE_STATUS_INFO[u"启用"]:
            return cs.LINE_STATUS_ERR, None

        # 验证线路是否在推荐的线路集合内
        push_line_list = rget(push_line(cargo_order_number))
        if push_line_list:
            push_line_list = json.loads(push_line_list)
        else:
            push_line_list = []

        if line_code not in push_line_list:
            return cs.LINE_PUSH_ERR, {'line_code': line_code}
        # 插入线路编号
        cargo_order_obj.fk_line_code = line_code
        db.session.commit()
        # insert line_volume
        code = line_volume_set(line_code, cargo_order_obj.cargo_volume, cargo_order_obj.cargo_weight, user['id'])
        if code is not cs.OK:
            logger.error(
                'insert line volume err line_name:{}, cargo_order_number:{}'.format(line_code, cargo_order_number))
        # 清空key
        delete(push_line(cargo_order_number))
        return cs.OK, {'cargo_order_number': cargo_order_number}
    except:
        logger.error('cargo_choose_line err {}'.format(traceback.format_exc(), ))
        raise
    finally:
        db.session.rollback()
