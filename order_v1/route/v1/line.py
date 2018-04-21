#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/25 23:01
# @Author  : Xsh
# @File    : line.py
# @Software: PyCharm

from flask import Blueprint, request
from tools.wraps import validate_params
from tools.response_tools import resp_wrapper as rw
from tools.request_tools import request_data
from service import line as Line
from log.info import logger

line = Blueprint('line', __name__)


@line.before_request
def before_request():
    pass


@line.teardown_request
def teardown_request(err):
    pass


@line.route('/id', methods=['POST'])
@validate_params(required=[('origin_code', unicode), ('destination_code', unicode), ('line_status', int, (1, 2)),
                           ('line_type', int, (1, 2)), ('line_kilometre', int), ('line_runtime', int),
                           ('location_list', list)])
def create_line():
    logger.debug('/order/line/id request data: {}'.format(request.values.items()))
    token = unicode(request_data().get('token'))
    origin_code = unicode(request_data().get('origin_code'))
    destination_code = unicode(request_data().get('destination_code'))
    line_status = int(request_data().get('line_status'))
    line_type = int(request_data().get('line_type'))
    line_kilometre = int(request_data().get('line_kilometre'))
    line_runtime = int(request_data().get('line_runtime'))
    location_list = list(request_data().get('location_list'))
    code, result = Line.create_line(token, origin_code, destination_code, line_status, line_type, line_kilometre,
                                    line_runtime, location_list)
    return rw(code, result)


@line.route('/ids', methods=['GET'])
@validate_params(required=[('page_size', int), ('page_index', int)])
def get_lines():
    logger.debug('/order/line/ids request data: {}'.format(request.values.items()))
    token = unicode(request_data().get('token'))
    line_code = unicode(request_data().get('line_code'))
    origin_code = unicode(request_data().get('origin_code'))
    destination_code = unicode(request_data().get('destination_code'))
    line_status = request_data().get('line_status')
    line_type = request_data().get('line_type')
    page_index = int(request_data().get('page_index'))
    page_size = int(request_data().get('page_size'))
    code, result = Line.get_lines(token, line_code, origin_code, destination_code, line_status,
                                  line_type, page_index, page_size)
    return rw(code, result)


@line.route('/id/modify', methods=['POST'])
@validate_params(required=[('line_code', unicode)])
def modify_line():
    logger.debug('/order/line/id/modify request data: {}'.format(request.values.items()))
    token = unicode(request_data().get('token'))
    line_code = unicode(request_data().get('line_code'))
    line_status = request_data().get('line_status')
    line_type = request_data().get('line_type')
    code, result = Line.modify_line(token, line_code, line_status, line_type)
    return rw(code, result)


@line.route('/id/line_locations', methods=['GET'])
@validate_params(required=[])
def get_line_locations():
    logger.debug('/order/line/id/line_locations request data: {}'.format(request.values.items()))
    token = unicode(request_data().get('token'))
    origin_code = unicode(request_data().get('origin_code'))
    destination_code = unicode(request_data().get('destination_code'))
    location_code = unicode(request_data().get('location_code'))
    location_status = request_data().get('location_status')
    page_index = int(request_data().get('page_index'))
    page_size = int(request_data().get('page_size'))
    code, rasult = Line.get_line_locations(token, origin_code, destination_code, location_code, location_status,
                                           page_index, page_size)
    return rw(code, rasult)


@line.route('/id/lines', methods=['GET'])
@validate_params(required=[('line_code', unicode)])
def get_line():
    logger.debug('/order/line/id/get_line request data: {}'.format(request.values.items()))
    token = unicode(request_data().get('token'))
    line_code = unicode(request_data().get('line_code'))
    code, rasult = Line.get_line(token, line_code)
    return rw(code, rasult)


@line.route('/id/codes', methods=['GET'])
@validate_params(required=[('chars', unicode)])
def get_line_names():
    logger.debug('/order/line/id/line_names request data: {}'.format(request.values.items()))
    token = unicode(request_data().get('token'))
    chars = unicode(request_data().get('chars'))
    code, rasult = Line.get_line_names(token, chars)
    return rw(code, rasult)
