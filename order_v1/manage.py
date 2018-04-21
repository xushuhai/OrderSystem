#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/14 14:10
# @Author  : Xsh
# @File    : manage.py.py
# @Software: PyCharm

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from front_controller import *
from route.v1.auth import auth
from route.v1.cargo_order import cargo_order
from route.v1.line import line
from route.v1.location import location
from route.v1.truck import truck
from route.v1.waybill import waybill
from route.v1.home import home

manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

app.register_blueprint(auth, url_prefix='/order/auth')
app.register_blueprint(cargo_order, url_prefix='/order/cargo_order')
app.register_blueprint(line, url_prefix='/order/line')
app.register_blueprint(location, url_prefix='/order/location')
app.register_blueprint(truck, url_prefix='/order/truck')
app.register_blueprint(waybill, url_prefix='/order/waybill')
app.register_blueprint(home, url_prefix='')

if __name__ == '__main__':
    manager.run()
