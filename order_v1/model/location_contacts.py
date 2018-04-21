#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/21 10:55
# @Author  : Xsh
# @File    : location_contacts.py
# @Software: PyCharm

# from instance.order_app import db
from config.order_app import db
from model.base_func import BaseFunc


class LocationContacts(BaseFunc, db.Model):
    """ 网点联系人信息 """
    __tablename__ = 'location_contacts'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    fk_location_code = db.Column('fk_location_code', db.String(6))  # 网点编码
    contacts_name = db.Column('contacts_name', db.String(256))  # 网点联系人
    contacts_telephone = db.Column('contacts_telephone', db.String(11))  # 网点联系人号码
    create_time = db.Column('create_time', db.TIMESTAMP)  # 创建时间
    update_time = db.Column('update_time', db.TIMESTAMP)  # 更新时间

    def __init__(self, fk_location_code, contacts_name, contacts_telephone):
        BaseFunc.__init__(self)

        self.fk_location_code = fk_location_code
        self.contacts_name = contacts_name
        self.contacts_telephone = contacts_telephone