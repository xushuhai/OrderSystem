#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/18 09:55
# @Author  : Xsh
# @File    : auth.py
# @Software: PyCharm

import uuid
from flask import Blueprint, request, make_response
from tools.wraps import validate_params, cost_run
from tools import constant as cs
from tools.response_tools import resp_wrapper as rw
from tools.request_tools import request_data
from service import auth as Auth
from cache.helper import delete
from cache.keys import get_token
from log.info import logger

auth = Blueprint('auth', __name__)

@cost_run
@auth.before_request
def before_request():
    pass


@auth.teardown_request
def teardown_request(err):
    pass

@auth.route('/verifying', methods=['POST'])
@validate_params(required=[('telephone', unicode)])
def get_verifying_code():
    logger.debug('/order/auth/verifying request data: {}'.format(request.values.items()))
    telephone = unicode(request_data().get('telephone'))
    code, result = Auth.get_verifying_code(telephone)
    return rw(code, result)


@auth.route('/verifying', methods=['GET'])
@validate_params(required=[('telephone', unicode)])
def get_verifying_code_get():
    logger.debug('/order/auth/verifying request data: {}'.format(request.values.items()))
    telephone = unicode(request_data().get('telephone'))
    code, result = Auth.get_verifying_code(telephone)
    return rw(code, result)


@auth.route('/verifying', methods=['PUT'])
@validate_params(required=[('telephone', unicode)])
def get_verifying_code_put():
    logger.debug('/order/auth/verifying request data: {}'.format(request.values.items()))
    telephone = unicode(request_data().get('telephone'))
    code, result = Auth.get_verifying_code(telephone)
    return rw(code, result)


@auth.route('/register', methods=['POST'])
@validate_params(
    required=[('verifying_code', unicode), ('name', unicode), ('telephone', unicode), ('username', unicode),
              ('password', unicode), ('mobile', unicode),
              ('role_type', int, (7, 8, 9, 10, 11))])
def register_user():
    logger.debug('/order/auth/register request data: {}'.format(request.values.items()))
    verifying_code = unicode(request_data().get('verifying_code'))
    telephone = unicode(request_data().get('telephone'))
    name = unicode(request_data().get('name'))
    username = unicode(request_data().get('username'))
    password = unicode(request_data().get('password'))
    mobile = unicode(request_data().get('mobile'))
    role_type = int(request_data().get('role_type'))
    fk_location_code = unicode(request_data().get('fk_location_code'))
    fk_plate = unicode(request_data().get('fk_plate'))
    code, result = Auth.register_user(verifying_code, telephone, name, username, password, mobile, role_type,
                                      fk_location_code, fk_plate)
    return rw(code, result)


@auth.route('/login', methods=['POST'])
@validate_params(required=[('username', unicode), ('password', unicode)])
def web_login():
    logger.debug('/order/auth/login request data: {}'.format(request.values.items()))
    token = uuid.uuid1()
    username = unicode(request_data().get('username'))
    password = unicode(request_data().get('password'))
    err, user = Auth.get_user(username, password, key=token)
    if err:
        return rw(err, {})
    if 'hash' in user:
        del user['hash']
    return rw(cs.OK, dict({'token': token}, **user))


@auth.route('/logout', methods=['POST'])
@validate_params(required=[('token', unicode)])
def web_logout():
    logger.debug('/order/auth/logout request data: {}'.format(request.values.items()))
    token = unicode(request_data().get('token'))
    delete(get_token(token))
    return rw(cs.OK, {})


@auth.route('/modify_password', methods=['POST'])
@validate_params(required=[('username', unicode), ('old_password', unicode), ('new_password', unicode)])
def modify_password():
    logger.debug('/order/auth/modify_password request data: {}'.format(request.values.items()))

    username = unicode(request_data().get('username'))
    old_password = unicode(request_data().get('old_password'))
    new_password = unicode(request_data().get('new_password'))
    code, result = Auth.modify_password(username, old_password, new_password)
    return rw(code, result)


@auth.route('/reset_password', methods=['POST'])
@validate_params(required=[('username', unicode), ('new_password', unicode), ('verifying_code', int)])
def reset_password():
    logger.debug('/order/auth/reset_password request data: {}'.format(request.values.items()))

    username = unicode(request_data().get('username'))
    new_password = unicode(request_data().get('new_password'))
    verifying_code = unicode(request_data().get('verifying_code'))
    code, result = Auth.reset_password(username, new_password, verifying_code)
    return rw(code, result)


@auth.route('/idss', methods=['GET'])
@validate_params(required=[])
def return_id():
    return rw(1000, "success")
