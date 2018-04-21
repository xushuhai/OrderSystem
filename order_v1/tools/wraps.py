#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/18 10:01
# @Author  : Xsh
# @File    : wraps.py
# @Software: PyCharm

from functools import wraps
from flask import request
from request_tools import request_data

from tools.exceptions import ParamError
from log.info import logger
import time


def cost_run(f):
    """ get the func cost time """

    @wraps(f)
    def decorator(*args, **kwargs):
        start_t = time.time()
        func_return = f(*args, **kwargs)
        end_t = time.time()
        logger.info('Cost time:{}ms\n'.format(end_t - start_t))
        if hasattr(func_return, 'headers'):
            try:
                header = [("Access-Control-Allow-Origin", "*"), ('Access-Control-Allow-Methods', 'PUT,GET,POST,DELETE'),
                          ('Access-Control-Allow-Headers', "Referer, Accept, Origin, User-Agent")]
                func_return.headers.__dict__.get('_list').extend(header)
                # func_return.headers.__dict__.get('_list').addAll(header)
            except AttributeError, e:
                logger.warning(e)
        return func_return

    return decorator


def validate_params(required):
    """
    Check the input params

    :param required:
        type(list or tuple)
        item:
            :type(list oor tuple)
            length should be >= 2
            item[0]: key name
            item[1]: key type
            item[2]: scope of key's value(not must)
        example:
            required = [('fence_name', unicode),('trigger_time', int),('trigger_type', int, range(3)),('action', int, (1,2))]
    :return:
    """

    def _validate_params(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if not isinstance(required, (list, tuple)):
                raise TypeError, 'The params required must be list!'
            for req in required:
                if len(req) < 2:
                    raise ValueError, "The required's item length must >= 2!"
                # Check the key is Exist:
                try:
                    client_val = request_data()[req[0]]
                except KeyError, e:
                    raise ParamError('Key = {} required'.format(req[0]))
                client_val_type = req[1]
                # Check teh key's type:
                if not isinstance(client_val, client_val_type):
                    if isinstance(client_val, basestring):
                        try:
                            client_val = client_val_type(client_val)
                        except ValueError, e:
                            raise ParamError('Key = {} type err!'.format(req[0]))
                    else:
                        raise ParamError('Key = {} type err!'.format(req[0]))
                # Check the key's value is in pre-defined:
                if len(req) >= 3:
                    if client_val not in req[2]:
                        raise ParamError(
                            'Key = {} value = {} err!'.format(req[0], client_val))
            val = f(*args, **kwargs)
            return val

        return wrapper

    return _validate_params
