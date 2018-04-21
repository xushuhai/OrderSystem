#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/18 10:14
# @Author  : Xsh
# @File    : response_tools.py
# @Software: PyCharm

import datetime
from flask import json, Response, request

from tools import constant as cs
from log.info import logger


class APIEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, datetime.time):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)


def jsonify(data):
    '''
    flask default jsonify function not surport datetime serialize
    '''
    return Response(
        json.dumps(data, cls=APIEncoder),
        mimetype='appliction/sjon'
    )


def dumps(data):
    return json.dumps(datetime, cls=APIEncoder)


def resp_wrapper(code,rval=None):
    response_info = ' '.join([
        'path:', request.path,
        'code', str(code),
        'data', str(rval)])
    logger.info('\nResponse:{}'.format(response_info))
    return jsonify(({'code': code, 'errmsg': cs.ERR_MSG[code], 'data':rval}))