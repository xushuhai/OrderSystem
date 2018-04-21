#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/28 11:05
# @Author  : Xsh
# @File    : location.py
# @Software: PyCharm

from flask import Blueprint, request
from tools.wraps import validate_params
from tools.response_tools import resp_wrapper as rw
from tools.request_tools import request_data
from service import location as Location
from log.info import logger

location = Blueprint('location', __name__)


@location.before_request
def before_request():
    pass


@location.teardown_request
def teardown_request(err):
    pass


@location.route('/id', methods=['POST'])
@validate_params(required=[('location_name', unicode), ('province', unicode), ('city', unicode)])
def create_location():
    logger.debug('/order/location/id request data: {}'.format(request.values.items()))
    token = unicode(request_data().get('token'))
    location_name = unicode(request_data().get('location_name'))
    detailed_address = unicode(request_data().get('detailed_address'))
    lot = unicode(request_data().get('lot'))
    lat = unicode(request_data().get('lat'))
    province = unicode(request_data().get('province'))
    city = unicode(request_data().get('city'))
    location_contactss = list(request_data().get('location_contactss'))
    code, result = Location.create_location(token, location_name, detailed_address, lot, lat, province, city,
                                            location_contactss)
    return rw(code, result)


@location.route('/ids', methods=['GET'])
@validate_params(required=[('page_size', int), ('page_index', int)])
def get_location_infos():
    logger.debug('/order/location/ids request data: {}'.format(request.values.items()))
    token = unicode(request_data().get('token'))
    location_code = unicode(request_data().get('location_code'))
    province = unicode(request_data().get('province'))
    city = unicode(request_data().get('city'))
    location_status = request_data().get('location_status')
    page_index = int(request_data().get('page_index'))
    page_size = int(request_data().get('page_size'))
    code, result = Location.get_location_infos(token, location_code, province, city, location_status, page_index,
                                               page_size)
    return rw(code, result)


@location.route('/ids/codes', methods=['GET'])
@validate_params(required=[('chars', unicode)])
def get_location_names():
    logger.debug('/order/location/ids/codes request data: {}'.format(request.values.items()))
    token = unicode(request_data().get('token'))
    chars = unicode(request_data().get('chars'))
    code, result = Location.get_location_names(token, chars)
    return rw(code, result)


@location.route('/id', methods=['GET'])
@validate_params(required=[('location_code', unicode)])
def get_location_info():
    logger.debug('/order/location/id request data: {}'.format(request.values.items()))
    token = unicode(request_data().get('token'))
    location_code = unicode(request_data().get('location_code'))
    code, result = Location.get_location_info(token, location_code)
    return rw(code, result)


@location.route('/id/modify', methods=['POST'])
@validate_params(required=[('location_code', unicode)])
def modify_location_info():
    logger.debug('/order/location/id request data: {}'.format(request.values.items()))
    token = unicode(request_data().get('token'))
    location_code = unicode(request_data().get('location_code'))
    location_name = unicode(request_data().get('location_name'))
    detailed_address = unicode(request_data().get('detail_address'))
    lot = unicode(request_data().get('lot'))
    lat = unicode(request_data().get('lat'))
    code, result = Location.modify_location_info(token, location_code, location_name, detailed_address, lot, lat)
    return rw(code, result)


@location.route('/id/enabled_disable', methods=['POST'])
@validate_params(required=[('location_code', unicode), ('location_status', int, (1, 2))])
def genabled_disable_location_info():
    logger.debug('/order/location/id/enabled_disable request data: {}'.format(request.values.items()))
    token = unicode(request_data().get('token'))
    location_code = unicode(request_data().get('location_code'))
    location_status = int(request_data().get('location_status'))
    code, result = Location.enabled_disable_location(token, location_code, location_status)
    return rw(code, result)
