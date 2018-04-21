#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/4 14:01
# @Author  : Xsh
# @File    : truck.py
# @Software: PyCharm


from flask import Blueprint, request
from tools.wraps import validate_params
from tools.response_tools import resp_wrapper as rw
from tools.request_tools import request_data
from service import truck as Truck
from log.info import logger

truck = Blueprint('truck', __name__)


@truck.before_request
def before_request():
    pass


@truck.teardown_request
def teardown_request(err):
    pass


@truck.route('/id', methods=['POST'])
@validate_params(required=[('plate', unicode), ('status', int, (1, 2)), ('plate_type', int, (1, 2, 3)),
                           ('vehicle_type', int, (1, 2)), ('container_type', int, (1, 2)),
                           ('container_length', int, xrange(0, 99999)),
                           ('container_wide', int, xrange(0, 99999)), ('container_high', int, xrange(0, 99999)),
                           ('container_volume', int, xrange(0, 99999))])
def create_truck():
    logger.debug('/order/truck/id request data: {}'.format(request.values.items()))
    token = unicode(request_data().get('token'))
    plate = unicode(request_data().get('plate'))
    status = int(request_data().get('status'))
    plate_type = int(request_data().get('plate_type'))
    vehicle_type = int(request_data().get('vehicle_type'))
    container_type = int(request_data().get('container_type'))
    container_length = int(request_data().get('container_length'))
    container_wide = int(request_data().get('container_wide'))
    container_high = int(request_data().get('container_high'))
    container_volume = int(request_data().get('container_volume'))
    code, result = Truck.create_truck(token, plate, status, plate_type, vehicle_type, container_type, container_length,
                                      container_wide, container_high, container_volume)
    return rw(code, result)


@truck.route('/ids', methods=['GET'])
@validate_params(required=[('page_size', int), ('page_index', int)])
def get_truck_infos():
    logger.debug('/order/truck/ids request data: {}'.format(request.values.items()))
    token = unicode(request_data().get('token'))
    plate = unicode(request_data().get('plate'))
    status = unicode(request_data().get('status'))
    plate_type = unicode(request_data().get('plate_type'))
    vehicle_type = request_data().get('vehicle_type')
    container_type = request_data().get('container_type')
    page_index = int(request_data().get('page_index'))
    page_size = int(request_data().get('page_size'))
    code, result = Truck.get_truck_infos(token, plate, status, plate_type, vehicle_type, container_type, page_index,
                                         page_size)
    return rw(code, result)


@truck.route('/ids/codes', methods=['GET'])
@validate_params(required=[('chars', unicode)])
def get_truck_plate():
    logger.debug('/order/truck/ids/codes request data: {}'.format(request.values.items()))
    token = unicode(request_data().get('token'))
    chars = unicode(request_data().get('chars'))
    code, result = Truck.get_truck_plates(token, chars)
    return rw(code, result)


@truck.route('/id', methods=['GET'])
@validate_params(required=[('plate', unicode)])
def get_truck_info():
    logger.debug('/order/truck/id request data: {}'.format(request.values.items()))
    token = unicode(request_data().get('token'))
    plate = unicode(request_data().get('plate'))
    code, result = Truck.get_truck_info(token, plate)
    return rw(code, result)


@truck.route('/id/modify', methods=['POST'])
@validate_params(required=[('plate', unicode)])
def modify_truck_info():
    logger.debug('/order/truck/id/modify request data: {}'.format(request.values.items()))
    token = unicode(request_data().get('token'))
    plate = unicode(request_data().get('plate'))
    container_type = unicode(request_data().get('container_type'))
    plate_type = unicode(request_data().get('plate_type'))
    vehicle_type = unicode(request_data().get('vehicle_type'))
    container_length = unicode(request_data().get('container_length'))
    container_wide = unicode(request_data().get('container_wide'))
    container_high = unicode(request_data().get('container_high'))
    container_volume = unicode(request_data().get('container_volume'))
    status = unicode(request_data().get('status'))
    code, result = Truck.modify_truck(token, plate, container_type, plate_type, vehicle_type, container_length,
                                      container_wide,
                                      container_high, container_volume, status)
    return rw(code, result)


@truck.route('/id/enabled_disable', methods=['POST'])
@validate_params(required=[('plate', unicode), ('status', int, (1, 2))])
def genabled_disable_truck_status():
    logger.debug('/order/truck/id/enabled_disable request data: {}'.format(request.values.items()))
    token = unicode(request_data().get('token'))
    plate = unicode(request_data().get('plate'))
    status = int(request_data().get('status'))
    code, result = Truck.enabled_disable_truck(token, plate, status)
    return rw(code, result)
