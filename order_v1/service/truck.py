#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/3 15:26
# @Author  : Xsh
# @File    : truck.py
# @Software: PyCharm

import traceback
import datetime

from config.order_app import db
from model.truck import Truck
from cache.helper import hgetall
from cache.keys import get_token
from tools import constant as cs
from log.info import logger


def get_truck_plates(token, chars):
    """
    线路模糊查询
    :param token:
    :param chars:
    :return:cs.OK, list
    """
    user = hgetall(get_token(token))
    if not user:
        return cs.AUTH_ERROR, None
    trucks = db.session.query(Truck.plate).distinct().filter(
        Truck.plate.like('%' + str(chars) + '%')).all()
    truck_list = []
    for truck in trucks:
        truck_list.append({'plate': truck.plate})
    return cs.OK, truck_list


def create_truck(token, plate, status, plate_type, vehicle_type, container_type, container_length, container_wide,
                 container_high, container_volume):
    """
    新增车辆
    :param token:
    :param plate:
    :param status:
    :param plate_type:
    :param vehicle_type:
    :param container_type:
    :param container_length:
    :param container_wide:
    :param container_high:
    :param container_volume:
    :return:cs.OK, dict
    """
    try:
        user = hgetall(get_token(token))
        if (not user) or int(user['role_type']) != cs.USER_ROLE_INFO[u"运单统筹专员"]:
            return cs.AUTH_ERROR, None
        # 验证车牌
        truck_obj = Truck.query.filter_by(plate=plate).first()
        if truck_obj:
            return cs.PLATE_EXIST, {'plate': plate}

        truck = Truck(plate, status, plate_type, vehicle_type, container_type, container_length, container_wide,
                      container_high, container_volume, user['id'])
        db.session.add(truck)
        db.session.commit()
        return cs.OK, {'plate': plate}
    except:
        logger.error('create truck err:{}'.format(traceback.format_exc(), ))
        raise
    finally:
        db.session.rollback()


def get_truck_infos(token, plate, status, plate_type, vehicle_type, container_type, page_index,
                    page_size):
    """
    车辆列表查询
    :param token:
    :param plate:
    :param status:
    :param plate_type:
    :param vehicle_type:
    :param container_type:
    :param page_index:
    :param page_size:
    :return:cs.OK, dict
    """
    user = hgetall(get_token(token))
    if not user:
        return cs.AUTH_ERROR, None
    statment = '1=1'

    if plate:
        statment += " and (truck.plate = '%s')" % plate
    if status:
        statment += " and (truck.status = '%s')" % status
    else:
        statment += " and (truck.status = '%s')" % cs.TRUCK_STATUS_INFO[u"启用"]
    if plate_type:
        statment += " and (truck.plate_type = '%s')" % plate_type
    if vehicle_type:
        statment += " and (truck.vehicle_type = '%s')" % vehicle_type
    if container_type:
        statment += " and (truck.container_type = '%s')" % container_type

    truck_objs = Truck.query.filter(statment).order_by(Truck.update_time.desc()).paginate(page_index, page_size,
                                                                                          False).items
    logger.info('get_trucks statment is {}'.format(statment, ))
    truck_count = db.session.query(Truck.id).filter(statment).count()
    rasult = {'truck_objs': [], 'truck_count': truck_count}
    for item in truck_objs:
        truck = {}
        truck['plate'] = item.plate
        truck['status'] = item.status
        truck['plate_type'] = item.plate_type
        truck['vehicle_type'] = item.vehicle_type
        truck['container_type'] = item.container_type
        truck['container_volume'] = item.container_volume
        rasult['truck_objs'].append(truck)
    return cs.OK, rasult


def get_truck_info(token, plate):
    """
    车辆信息查询
    :param token:
    :param plate:
    :return:cs.OK, object
    """
    user = hgetall(get_token(token))
    if not user:
        return cs.AUTH_ERROR, None

    truck_obj = Truck.query.filter_by(plate=plate).first()
    if truck_obj:
        truck = {}
        truck['plate'] = truck_obj.plate
        truck['container_type'] = truck_obj.container_type
        truck['plate_type'] = truck_obj.plate_type
        truck['vehicle_type'] = truck_obj.vehicle_type
        truck['container_length'] = truck_obj.container_length
        truck['container_wide'] = truck_obj.container_wide
        truck['container_high'] = truck_obj.container_high
        truck['container_volume'] = truck_obj.container_volume
        truck['status'] = truck_obj.status
        return cs.OK, truck
    else:
        return cs.PLATE_ERR, {'plate': plate}


def modify_truck(token, plate, container_type, plate_type, vehicle_type, container_length, container_wide,
                 container_high, container_volume, status):
    """
    修改车辆信息
    :param token:
    :param plate:
    :param container_type:
    :param plate_type:
    :param vehicle_type:
    :param container_length:
    :param container_wide:
    :param container_high:
    :param container_volume:
    :param status:
    :return: cs.OK,dict
    """
    try:
        user = hgetall(get_token(token))
        if (not user) or int(user['role_type']) != cs.USER_ROLE_INFO[u"运单统筹专员"]:
            return cs.AUTH_ERROR, None
        truck_obj = Truck.query.filter_by(plate=plate).first()
        if not truck_obj:
            return cs.PLATE_ERR, {'plate': plate}
        truck_obj.container_type = container_type
        truck_obj.plate_type = plate_type
        truck_obj.vehicle_type = vehicle_type
        truck_obj.container_length = container_length
        truck_obj.container_wide = container_wide
        truck_obj.container_high = container_high
        truck_obj.container_volume = container_volume
        truck_obj.status = status
        truck_obj.update_time = datetime.datetime.now()
        db.session.commit()
        return cs.OK, {'plate': plate}
    except:
        logger.error('modify truck err:{}'.format(traceback.format_exc(), ))
        raise
    finally:
        db.session.rollback()


def enabled_disable_truck(token, plate, status):
    """
    启用禁用车辆
    :param token:
    :param plate:
    :param status:
    :return: cs.OK, dict
    """
    user = hgetall(get_token(token))
    if (not user) or int(user['role_type']) != cs.USER_ROLE_INFO[u"运单统筹专员"]:
        return cs.AUTH_ERROR, None
    try:
        truck_obj = Truck.query.filter_by(plate=plate).first()
        if truck_obj:
            truck_obj.status = status
            truck_obj.update_time = datetime.datetime.now()
            db.session.commit()
            return cs.OK, {'plate': plate}
        else:
            return cs.PLATE_ERR, {'plate': plate}
    except:
        logger.error("modify line err : {}".format(traceback.format_exc(), ))
        raise
    finally:
        db.session.rollback()
