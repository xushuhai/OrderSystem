#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/18 15:35
# @Author  : Xsh
# @File    : front_controller.py
# @Software: PyCharm

import json
import sqlalchemy.exc
from flask import request, abort
from kombu.exceptions import InconsistencyError
from redis.exceptions import ConnectionError
# from instance.order_app import app, db
from config.order_app import db, app
from log.info import logger
from tools import constant as cs
from tools.exceptions import (ParamError, AuthError)
from tools.request_tools import request_data
from tools.response_tools import resp_wrapper as rw
from tools.wraps import cost_run
from cache.helper import rexpire, hgetall
from cache.keys import get_token
from config.test import EXPIRE_TIME, FILTER_AUTH


@cost_run
@app.before_request
def before_request():
    request_infos = ''.join([
        request.method, 'path:', request.path, str(request_data())
    ])
    logger.info('request endpoint : %s' % (request.endpoint))
    logger.info('request url : %s' % (request.path))
    logger.info('request headers: %s' % (request.headers.items()))
    logger.info('request GET  data: %s' % (request.values.items()))
    logger.info('request POST data: %s' % (request.data))
    logger.info('\nrequest:{}'.format(request_infos))
    if request.path == '/':
        pass
    else:
        _in = False
        for item in FILTER_AUTH:
            if request.path.find(item) == 0:
                _in = True
                break
        if False == _in:
            token = unicode(request_data().get('token'))
            if not token:
                abort(400)
            rexpire(get_token(token), EXPIRE_TIME)
            user = hgetall(get_token(token))
            if not user:
                abort(401)
            if user and int(user['role_type']) not in cs.USER_ROLE_TYPE.keys():
                abort(403)


@app.teardown_request
def teardown_request(exception):
    db.session.remove()


@app.errorhandler(ParamError)
def params_exception(e):
    logger.exception('PARAMS_ERR:{}'.format(e))
    return rw(cs.PARAMS_ERROR, e.value)


@app.errorhandler(AuthError)
def auth_exception(e):
    logger.exception('AuthError:{}'.format(e))
    return rw(cs.AUTH_ERROR, e.value)


@app.errorhandler(ConnectionError)
def cache_exception(e):
    logger.error('Redis Exception:{}'.format(e))
    return rw(cs.DB_ERROR)


@app.errorhandler(InconsistencyError)
def celery_exception(e):
    logger.warning('Celery Exception:{}'.format(e))
    return rw(cs.OK)


@app.errorhandler(sqlalchemy.exc.DBAPIError)
def db_exception(e):
    logger.exception('Db Exception:{}'.format(e))
    db.session.rollback()
    return rw(cs.DB_ERROR)


@app.errorhandler(Exception)
def unhandled_exception(e):
    logger.exception('Unhandled Exception:{}'.format(e))
    return rw(cs.SERVER_ERR)
