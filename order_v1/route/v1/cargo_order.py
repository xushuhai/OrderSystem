#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/22 15:42
# @Author  : Xsh
# @File    : cargo_order.py
# @Software: PyCharm

from flask import Blueprint, request
from tools.wraps import validate_params
from tools.response_tools import resp_wrapper as rw
from tools.request_tools import request_data
from service import cargo_order as Corder
from log.info import logger

cargo_order = Blueprint('cargo_order', __name__)


@cargo_order.before_request
def before_request():
    pass


@cargo_order.teardown_request
def teardown_request(err):
    pass


@cargo_order.route('/id', methods=['POST'])
@validate_params(required=[('origin_code', unicode), ('destination_code', unicode), ('cargo_name', unicode),
                           ('cargo_volume', unicode), ('cargo_weight', unicode),
                           ('specified_arrival_time', unicode), ('consignor_name', unicode),
                           ('consignor_telephone', unicode), ('consignee_name', unicode),
                           ('consignee_telephone', unicode)])
def create_cargo_order():
    logger.debug('/order/cargo_order/id request data: {}'.format(request.values.items()))
    token = unicode(request_data().get('token'))
    origin_code = unicode(request_data().get('origin_code'))
    destination_code = unicode(request_data().get('destination_code'))
    cargo_name = unicode(request_data().get('cargo_name'))
    cargo_volume = unicode(request_data().get('cargo_volume'))
    cargo_weight = unicode(request_data().get('cargo_weight'))
    specified_arrival_time = unicode(request_data().get('specified_arrival_time'))
    consignor_name = unicode(request_data().get('consignor_name'))
    consignor_telephone = unicode(request_data().get('consignor_telephone'))
    consignee_name = unicode(request_data().get('consignee_name'))
    consignee_telephone = unicode(request_data().get('consignee_telephone'))
    code, result = Corder.create_cargo_order(token, origin_code, destination_code, cargo_name, cargo_volume,
                                             cargo_weight, specified_arrival_time, consignor_name, consignor_telephone,
                                             consignee_name, consignee_telephone)
    return rw(code, result)


@cargo_order.route('/ids', methods=['GET'])
@validate_params(required=[('start_date', unicode), ('end_date', unicode), ('page_index', int), ('page_size', int)])
def get_cargo_orders():
    logger.debug('/order/cargo_order/ids request data: {}'.format(request.values.items()))
    token = unicode(request_data().get('token'))
    start_date = unicode(request_data().get('start_date'))
    end_date = unicode(request_data().get('end_date'))
    order_status = unicode(request_data().get('order_status'))
    cargo_order_number = unicode(request_data().get('cargo_order_number'))
    origin_code = unicode(request_data().get('origin_code'))
    destination_code = unicode(request_data().get('destination_code'))
    page_index = unicode(request_data().get('page_index'))
    page_size = unicode(request_data().get('page_size'))
    select_flag = unicode(request_data().get('select_flag'))
    code, result = Corder.get_cargo_orders(token, start_date, end_date, order_status, cargo_order_number, origin_code,
                                           destination_code, page_index, page_size, select_flag)
    return rw(code, result)

@cargo_order.route('/id', methods=['GET'])
@validate_params(required=[('cargo_order_number', unicode)])
def get_cargo_order():
    logger.debug('/order/cargo_order/id request data: {}'.format(request.values.items()))
    token = unicode(request_data().get('token'))
    cargo_order_number = unicode(request_data().get('cargo_order_number'))
    code, result = Corder.get_cargo_order(token, cargo_order_number)
    return rw(code, result)



@cargo_order.route('/id/status', methods=['POST'])
@validate_params(required=[('cargo_order_number', unicode), ('cargo_order_status', unicode)])
def modify_order_status():
    logger.debug('/order/cargo_order/id/status request data: {}'.format(request.values.items()))
    token = unicode(request_data().get('token'))
    cargo_order_number = unicode(request_data().get('cargo_order_number'))
    cargo_order_status = unicode(request_data().get('cargo_order_status'))
    if 'remark' in request_data().keys():
        remark = unicode(request_data().get('remark'))
    else:
        remark = None
    code, result = Corder.modify_order_status(token, cargo_order_number, cargo_order_status, remark)
    return rw(code, result)


@cargo_order.route('/id/choose', methods=['POST'])
@validate_params(required=[('cargo_order_number', unicode), ('line_code', unicode)])
def cargo_choose_line():
    logger.debug('/order/cargo_order/id/choose request data: {}'.format(request.values.items()))
    token = unicode(request_data().get('token'))
    cargo_order_number = unicode(request_data().get('cargo_order_number'))
    line_code = unicode(request_data().get('line_code'))
    code, result = Corder.cargo_choose_line(token, cargo_order_number, line_code)
    return rw(code, result)



