#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/9 14:37
# @Author  : Xsh
# @File    : waybill.py
# @Software: PyCharm

from flask import Blueprint, request
from tools.wraps import validate_params
from tools.response_tools import resp_wrapper as rw
from tools.request_tools import request_data
from service import waybill as Waybill
from log.info import logger

waybill = Blueprint('waybill', __name__)


@waybill.before_request
def before_request():
    pass


@waybill.teardown_request
def teardown_request(err):
    pass


@waybill.route('/id', methods=['POST'])
@validate_params(
    required=[('line_no', unicode), ('plate', unicode), ('driver_name', unicode), ('driver_telephone', unicode),
              ('cargo_order_numbers', list)])
def create_waybill():
    logger.debug('/order/waybill/id request data: {}'.format(request.values.items()))
    token = unicode(request_data().get('token'))
    line_no = unicode(request_data().get('line_no'))
    start_time = unicode(request_data().get('start_time'))
    end_time = unicode(request_data().get('end_time'))
    plate = unicode(request_data().get('plate'))
    driver_name = unicode(request_data().get('driver_name'))
    driver_telephone = unicode(request_data().get('driver_telephone'))
    remarks = unicode(request_data().get('remarks'))
    cargo_order_numbers = list(request_data().get('cargo_order_numbers'))
    code, result = Waybill.create_waybill(token, line_no, start_time, end_time, plate, driver_name, driver_telephone,
                                          remarks, cargo_order_numbers)
    return rw(code, result)


@waybill.route('/id/modify', methods=['POST'])
@validate_params(
    required=[('waybill_number', unicode), ('plate', unicode), ('driver_name', unicode), ('driver_telephone', unicode),
              ('start_time', unicode), ('end_time', unicode), ('cargo_order_numbers', list), ('remarks', unicode)])
def modify_waybill():
    logger.debug('/order/waybill/id/modify request data: {}'.format(request.values.items()))
    token = unicode(request_data().get('token'))
    waybill_number = unicode(request_data().get('waybill_number'))
    plate = unicode(request_data().get('plate'))
    driver_name = unicode(request_data().get('driver_name'))
    driver_telephone = unicode(request_data().get('driver_telephone'))
    start_time = unicode(request_data().get('start_time'))
    end_time = unicode(request_data().get('end_time'))
    cargo_order_numbers = list(request_data().get('cargo_order_numbers'))
    remarks = unicode(request_data().get('remarks'))
    code, result = Waybill.modify_waybill(token, waybill_number, plate, driver_name, driver_telephone, start_time,
                                          end_time, cargo_order_numbers, remarks)
    return rw(code, result)


@waybill.route('/id/modify_status', methods=['POST'])
@validate_params(
    required=[('waybill_number', unicode), ('waybill_status', int, (200, 300, 500))])
def modify_waybill_status():
    logger.debug('/order/waybill/id/modify_status request data: {}'.format(request.values.items()))
    token = unicode(request_data().get('token'))
    waybill_number = unicode(request_data().get('waybill_number'))
    waybill_status = int(request_data().get('waybill_status'))
    code, result = Waybill.modify_waybill_status(token, waybill_number, waybill_status)
    return rw(code, result)


@waybill.route('/id/modify_type', methods=['POST'])
@validate_params(
    required=[('waybill_number', unicode), ('waybill_type', int, (1, 2, 3)), ('remarks', unicode)])
def modify_waybill_type():
    logger.debug('/order/waybill/id/modify_type request data: {}'.format(request.values.items()))
    token = unicode(request_data().get('token'))
    waybill_number = unicode(request_data().get('waybill_number'))
    waybill_type = int(request_data().get('waybill_type'))
    remarks = unicode(request_data().get('remarks'))
    code, result = Waybill.modify_waybill_type(token, waybill_number, waybill_type, remarks)
    return rw(code, result)
