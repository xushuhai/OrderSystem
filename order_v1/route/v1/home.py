#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/24 09:41
# @Author  : Xsh
# @File    : home.py
# @Software: PyCharm

from flask import Blueprint, request, render_template
from tools.wraps import validate_params
from log.info import logger

home = Blueprint('home', __name__)


@home.before_request
def before_request():
    pass


@home.teardown_request
def teardown_request(err):
    pass


@home.route('/', methods=['GET'])
@validate_params(required=[])
def index():
    logger.debug('/ request data: {}'.format(request.values.items()))
    # return redirect(url_for())
    return "hello world "
