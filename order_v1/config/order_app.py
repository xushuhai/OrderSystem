#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/14 14:16
# @Author  : Xsh
# @File    : order_app.py
# @Software: PyCharm

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config.test import CONFIG_NAME, SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS


app = Flask(__name__, instance_relative_config=True)
app.debug = True
app.config.from_pyfile(CONFIG_NAME, silent=True)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
app.config['SQLALCHEMY_ECHO'] = False
db = SQLAlchemy(app)
