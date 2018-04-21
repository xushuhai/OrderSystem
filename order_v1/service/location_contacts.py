#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/30 10:23
# @Author  : Xsh
# @File    : location_contacts.py
# @Software: PyCharm

import traceback

from cache.helper import hgetall
from cache.keys import get_token
from config.order_app import db
from tools import constant as cs

from model.location_contacts import LocationContacts as LC
from log.info import logger


def get_location_contacts(location_code):
    """
    获取转运中心联系人
    :param location_code:
    :return:list
    """
    location_contacts = LC.query.filter_by(fk_location_code=location_code).all()
    contacts = []
    for item in location_contacts:
        contact = {}
        contact['contact_name'] = item.contacts_name
        contact['contact_telephone'] = item.contacts_telephone
        contacts.append(contact)
    return contacts


def modify_location(token, location_list):
    """
    修改转运中心联系人
    :param token:
    :param location_list:
    :return: cs.OK, None
    """
    user = hgetall(get_token(token))
    if (not user) or int(user['role_type']) != cs.USER_ROLE_INFO[u"线路规划专员"]:
        return cs.AUTH_ERROR, None

    if location_list:
        try:
            for location in location_list:
                location_obj = LC.query.filter_by(fk_location_code=location['location_code'], contacts_name='').first()
                if location_obj:
                    location_obj.contacts_name = location['contacts_name']
                    location_obj.contacts_telephone = location['contacts_telephone']
            db.session.commit()
            return cs.OK, None
        except:
            logger.error("modify location err : {}".format(traceback.format_exc(), ))
            raise
        finally:
            db.session.rollback()
