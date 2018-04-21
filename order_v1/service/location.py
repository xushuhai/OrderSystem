#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/22 13:53
# @Author  : Xsh
# @File    : location.py
# @Software: PyCharm

import traceback
from datetime import datetime
from model.location import Location
from model.location_count import LocationCount as Lcount
from model.location_contacts import LocationContacts as LC
from config.order_app import db
from tools import constant as cs
from cache.helper import hgetall
from cache.keys import get_token
from log.info import logger
from location_contacts import get_location_contacts


def generate_location_code():
    """
    生成转运网点编号
    :return:location_code
    """
    location_count_obj = Lcount.query.filter_by().first()
    if location_count_obj:
        location_amount = location_count_obj.location_amount + 1
        location_count_obj.location_amount = location_amount
        location_count_obj.update_time = datetime.now()
    else:
        location_amount = 1
        location_count_new = Lcount(location_amount)
        db.session.add(location_count_new)
    db.session.commit()
    amounter = str(location_amount).zfill(5)
    return 'LT{}'.format(amounter)


def get_location_names(token, chars):
    """
    转运网点模糊查询
    :param chars:
    :return:cs.OK, list
    """
    user = hgetall(get_token(token))
    if not user:
        return cs.AUTH_ERROR, None
    locations = db.session.query(Location.location_code, Location.location_name).distinct().filter(
        Location.location_name.like('%' + str(chars) + '%'),
        Location.location_status == cs.LOCATION_STATUS_INFO[u"启用"]).all()
    locations_list = []
    for location in locations:
        locations_list.append({'code': location.location_code, 'name': location.location_name})
    return cs.OK, locations_list


def get_location(code):
    """
    根据转运网点code获取转运网点名称
    :param code:
    :return:
    """
    location = Location.query.filter_by(location_code=code).first()
    return location


def create_location(token, location_name, detailed_address, lot, lat, province, city, location_contactss):
    """
    创建转运网点
    :param token:
    :param location_name:
    :param detailed_address:
    :param lot:
    :param lat:
    :param province:
    :param city:
    :return:
    """
    user = hgetall(get_token(token))
    if (not user) or int(user['role_type']) != cs.USER_ROLE_INFO[u"线路规划专员"]:
        return cs.AUTH_ERROR, None
    # 生成location_code
    location_code = generate_location_code()
    try:
        location_obj = Location(location_name, location_code, detailed_address, lot, lat, province, city,
                                cs.LOCATION_STATUS_INFO[u"启用"])
        # 创建网点联系人
        if location_contactss:
            print location_contactss
            for item in location_contactss:
                location_contacts = LC(location_code, item['contacts_name'], item['contacts_telephone'])
                db.session.add(location_contacts)
        db.session.add(location_obj)
        db.session.commit()
        return cs.OK, location_code
    except:
        logger.error("create location err : {}".format(traceback.format_exc(), ))
        raise
    finally:
        db.session.rollback()


def get_location_infos(token, location_code, province, city, location_status, page_index, page_size):
    """
    转运网点列表
    :param token:
    :param location_code:
    :param province:
    :param city:
    :param location_status:
    :return:
    """
    user = hgetall(get_token(token))
    if (not user) or int(user['role_type']) != cs.USER_ROLE_INFO[u"线路规划专员"]:
        return cs.AUTH_ERROR, None
    statment = '1=1'

    if location_code:
        statment += " and (location.location_code = '%s')" % location_code
    if province:
        statment += " and (location.province = '%s')" % province
    if city:
        statment += " and (location.city = '%s')" % city
    if location_status:
        statment += " and (location.location_status = '%s')" % location_status
    else:
        statment += " and (location.location_status = '%s')" % cs.LOCATION_STATUS_INFO[u"启用"]

    location_objs = Location.query.filter(statment).order_by(Location.update_time.desc()).paginate(page_index,
                                                                                                   page_size,
                                                                                                   False).items
    # location_objs = Location.query.filter(statment).order_by(Location.update_time.desc())
    logger.info('get_lines statment is {}'.format(statment, ))
    locations_count = db.session.query(Location.id).filter(statment).count()
    rasult = {'location_objs': [], 'location_count': locations_count}
    for item in location_objs:
        location = {}
        location['location_code'] = item.location_code
        location['location_name'] = item.location_name
        location['province'] = item.province
        location['city'] = item.city
        location['location_status'] = item.location_status
        rasult['location_objs'].append(location)
        print item.location_code

    return cs.OK, rasult


def get_location_info(token, location_code):
    """
    获取转运网点信息
    :param token:
    :param location_code:
    :return:
    """
    user = hgetall(get_token(token))
    if not user:
        return cs.AUTH_ERROR, None
    location = Location.query.filter_by(location_code=location_code).first()
    location_obj = {}
    if location:
        location_obj['location_code'] = location.location_code
        location_obj['location_name'] = location.location_name
        location_obj['detailed_address'] = location.detailed_address
        location_obj['lot'] = location.lot
        location_obj['lat'] = location.lat
        location_obj['province'] = location.province
        location_obj['city'] = location.city
        location_obj['location_status'] = location.location_status
        location_obj['create_time'] = location.create_time
        location_obj['location_contacts'] = get_location_contacts(location.location_code)

    return cs.OK, {'location_objs': location_obj}


def modify_location_info(token, location_code, location_name, detailed_address, lot, lat):
    """
    修改转运中心信息
    :param token:
    :param location_name:
    :param detailed_address:
    :param lot:
    :param lat:
    :return:cs.OK, location_code
    """
    user = hgetall(get_token(token))
    if (not user) or int(user['role_type']) != cs.USER_ROLE_INFO[u"线路规划专员"]:
        return cs.AUTH_ERROR, None
    try:
        location_obj = Location.query.filter_by(location_code=location_code).first()
        if location_obj:
            location_obj.location_name = location_name
            location_obj.detailed_address = detailed_address
            location_obj.lot = lot
            location_obj.lat = lat
            location_obj.update_time = datetime.now()
            db.session.commit()
            return cs.OK, location_code
        else:
            return cs.LOCATION_CODE_ERR, None
    except:
        logger.error("modify location err : {}".format(traceback.format_exc(), ))
        raise
    finally:
        db.session.rollback()


def enabled_disable_location(token, location_code, location_status):
    """
    启用禁用转运中心
    :param token:
    :param location_code:
    :param location_status:
    :return: cs.OK
    """
    user = hgetall(get_token(token))
    if (not user) or int(user['role_type']) != cs.USER_ROLE_INFO[u"线路规划专员"]:
        return cs.AUTH_ERROR, None
        # location_stauts 验证在route中
    # if location_status not in cs.LOCATION_STATUS_INDEX.keys():
    #     return cs.PARAMS_ERROR, {"look": 'look'}

        # 修改数据
    try:
        location_obj = Location.query.filter_by(location_code=location_code).first()
        if location_obj:
            location_obj.location_status = location_status
            db.session.commit()
            return cs.OK, location_code
        else:
            return cs.LOCATION_CODE_ERR, None
    except:
        logger.error("modify location err : {}".format(traceback.format_exc(), ))
        raise
    finally:
        db.session.rollback()
