#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/25 21:57
# @Author  : Xsh
# @File    : line.py
# @Software: PyCharm

import sys
import traceback

from config.order_app import db
from model.line import Line
from model.line_location import LineLocations

from tools import constant as cs
from cache.helper import hgetall
from cache.keys import get_token
from log.info import logger

from location import get_location

reload(sys)
sys.setdefaultencoding("utf-8")


def get_line_names(token, chars):
    """
    线路模糊查询
    :param token:
    :param chars:
    :return:
    """
    user = hgetall(get_token(token))
    if not user:
        return cs.AUTH_ERROR, None
    lines = db.session.query(Line.line_code, Line.line_name).distinct().filter(
        Line.line_name.like('%' + str(chars) + '%')).all()
    line_list = []
    for line in lines:
        line_list.append({'line_code': line.line_code, 'name': line.line_name})
    return cs.OK, line_list


def create_line(token, origin_code, destination_code, line_status, line_type, line_kilometre, line_runtime,
                location_list):
    """
    创建线路信息
    :param token:
    :param origin_code:
    :param destination_code:
    :param line_status:
    :param line_type:
    :param line_kilometre:
    :param line_runtime:
    :param location_list:
    :return: cs.OK, {}
    """
    try:
        user = hgetall(get_token(token))
        if (not user) or int(user['role_type']) != cs.USER_ROLE_INFO[u"线路规划专员"]:
            return cs.AUTH_ERROR, None
        # 验证始发地目的地
        origin_location = get_location(origin_code)
        destination_location = get_location(destination_code)
        if not origin_location and not destination_location:
            return cs.LOCATION_CODE_ERR, None

        # 验证径停点 空校验，正确性校验
        if not location_list:
            return cs.LOCATION_INFO_ERR, None
        for item in list(location_list):

            location = get_location(int(item['location_code']))
            if not location:
                return cs.LOCATION_CODE_ERR, {'location_code': item['location_code']}

        # 生成线路编码
        line_code = "MOT{}TO{}".format(origin_code, destination_code)
        line_code_count = db.session.query(Line.id).filter(
            Line.line_code.like('%' + str('MOT' + origin_code + 'TO' + destination_code) + '%')).count()
        amounter = str(line_code_count + 1).zfill(5)
        line_code = "{}{}".format(line_code, amounter)

        # 生成线路名称
        origin_name = origin_location.location_name
        destination_name = destination_location.location_name
        line_name = "{}-{}".format(origin_name, destination_name)
        location_number = len(location_list)
        # 添加线路信息
        line = Line(line_code, line_name, origin_code, destination_code, line_status, line_type, line_kilometre,
                    line_runtime, location_number, user['id'])

        # 添加径停点信息
        for item in location_list:
            line_location = LineLocations(line_code, origin_code, destination_code, item['location_code'],
                                          item['sequence'],
                                          cs.LINE_LOCATION_STATUS_INFO[u"启用"], user['id'])
            db.session.add(line_location)
        db.session.add(line)
        db.session.commit()
        return cs.OK, {'line_code': line_code}
    except:
        logger.error('create_line err:{}'.format(traceback.format_exc(), ))
        raise
    finally:
        db.session.rollback()


def get_lines(token, line_code, origin_code, destination_code, line_status, line_type, page_index,
              page_size):
    """
    货物线路列表
    :param token:
    :param line_code:
    :param origin_code:
    :param destination_code:
    :param line_status:
    :param line_type:
    :param page_index:
    :param page_size:
    :return: cs.OK,{}
    """
    user = hgetall(get_token(token))
    if (not user) or int(user['role_type']) not in cs.SELECT_LINE_ROLE:
        return cs.AUTH_ERROR, None
    statment = '1=1'

    if line_code:
        statment += " and (line.line_code = '%s')" % line_code
    if origin_code:
        statment += " and (line.origin_code = '%s')" % origin_code
    if destination_code:
        statment += " and (line.destination_code = '%s')" % destination_code
    if line_type:
        statment += " and (line.line_type = '%s')" % line_type
    if line_status:
        statment += " and (line.line_status = '%s')" % line_status
    else:
        statment += " and (line.line_status = '%s')" % cs.LINE_STATUS_INFO[u"启用"]

    lines_objs = Line.query.filter(statment).order_by(Line.update_time.desc()).paginate(page_index, page_size,
                                                                                        False).items
    logger.info('get_lines statment is {}'.format(statment, ))
    lines_count = db.session.query(Line.id).filter(statment).count()
    rasult = {'line_objs': [], 'line_count': lines_count}
    for item in lines_objs:
        line = {}
        line['line_code'] = item.line_code
        line['line_name'] = item.line_name
        line['origin_name'] = get_location(item.origin_code).location_name
        line['destination_code'] = get_location(item.destination_code).location_name
        line['line_kilometre'] = item.line_kilometre
        line['line_runtime'] = item.line_runtime
        line['location_number'] = item.location_number
        rasult['line_objs'].append(line)
    return cs.OK, rasult


def get_line_locations(token, origin_code, destination_code, location_code, location_status, page_index, page_size):
    """
    获取转运中心列表
    :param token:
    :param origin_code:
    :param destination_code:
    :param location_code:
    :param location_status:
    :param page_index:
    :param page_size:
    :return: cs.OK,{}
    """
    user = hgetall(get_token(token))
    if (not user) or int(user['role_type']) not in cs.SELECT_LINE_ROLE:
        return cs.AUTH_ERROR, None

    statment = '1=1'
    if origin_code:
        statment += " and (line_location.origin_code = '%s')" % origin_code

    if destination_code:
        statment += " and (line_location.destination_code = '%s')" % destination_code

    if location_code:
        statment += " and (line_location.location_code = '%s')" % location_code

    if location_status:
        statment += " and (line_location.location_status = '%s')" % location_status
    else:
        statment += " and (line_location.location_status = '%s')" % cs.LINE_STATUS_INFO[u"启用"]

    print statment
    line_locations = LineLocations.query.filter(statment).order_by(LineLocations.update_time.desc()).paginate(
        page_index,
        page_size,
        False).items
    lines_count = db.session.query(LineLocations.id).filter(statment).count()
    rasult = {'line_objs': [], 'line_count': lines_count}
    for item in line_locations:
        line = {}
        line_obj = Line.query.filter_by(line_code=item.fk_line_code).first()
        line['line_code'] = line_obj.line_code
        line['line_name'] = line_obj.line_name
        line['origin_name'] = get_location(line_obj.origin_code).location_name
        line['destination_code'] = get_location(line_obj.destination_code).location_name
        line['line_kilometre'] = line_obj.line_kilometre
        line['line_runtime'] = line_obj.line_runtime
        line['location_number'] = line_obj.location_number
        rasult['line_objs'].append(line)
    return cs.OK, rasult


def modify_line(token, line_code, line_status, line_type):
    """
    修改线路属性和状态
    :param token:
    :param line_code:
    :param line_status:
    :param line_type:
    :return: cs.OK,{}
    """
    user = hgetall(get_token(token))
    if (not user) or int(user['role_type']) != cs.USER_ROLE_INFO[u"线路规划专员"]:
        return cs.AUTH_ERROR, None
    try:
        # 验证线路编码
        line = Line.query.filter_by(line_code=line_code).first()
        if not line:
            return cs.LINE_CODE_ERR, {'line_code': line_code}
        if line_status:
            line_status = int(line_status)
            if line_status in cs.LINE_STATUS_INDEX.keys():
                line.line_status = line_status
                # 径停点同步改变
                line_locations = LineLocations.query.filter_by(fk_line_code=line_code).all()
                for item in line_locations:
                    item.location_status = line_status
            else:
                return cs.LINE_STATUS_ERR, None

        if line_type:
            line_type = int(line_type)
            if line_type in cs.LINE_TYPE_INDEX.keys():
                line.line_type = line_type
            else:
                return cs.LINE_TYPE_ERR, None
        db.session.commit()
        return cs.OK, {'line_code': line_code}
    except:
        logger.error("modify line err : {}".format(traceback.format_exc(), ))
        raise
    finally:
        db.session.rollback()


def get_line(token, line_code):
    """
    获取线路信息
    :param token:
    :param line_code:
    :return:
    """
    user = hgetall(get_token(token))
    if (not user) or int(user['role_type']) not in cs.SELECT_LINE_ROLE:
        return cs.AUTH_ERROR, None
    line_obj = Line.query.filter_by(line_code=line_code).first()
    if not line_obj:
        return cs.LINE_CODE_ERR, {'line_code': line_code}
    line = {}
    line['line_code'] = line_obj.line_code
    line['line_name'] = line_obj.line_name
    line['origin_name'] = get_location(line_obj.origin_code).location_name
    line['destination_name'] = get_location(line_obj.destination_code).location_name
    line['line_status'] = line_obj.line_status
    line['line_type'] = line_obj.line_type
    line['line_kilometre'] = line_obj.line_kilometre
    line['line_runtime'] = line_obj.line_runtime
    line['location_number'] = line_obj.location_number
    line['location_infos'] = []
    # 获取径停点信息
    location_objs = LineLocations.query.filter_by(fk_line_code=line_code).all()
    if location_objs:
        for item in location_objs:
            location_name = get_location(item.location_code).location_name
            line['location_infos'].append({'location_name': location_name, 'sequence': item.sequence})
    return cs.OK, line


def enabled_disable_line(token, line_code, line_status):
    """
    启用禁用线路
    :param token:
    :param line_code:
    :param line_status:
    :return: cs.OK,{}
    """
    user = hgetall(get_token(token))
    if (not user) or int(user['role_type']) != cs.USER_ROLE_INFO[u"线路规划专员"]:
        return cs.AUTH_ERROR, None
    try:
        line_obj = Line.query.filter_by(line_code=line_code).first()
        if line_obj:
            line_obj.line_status = line_status
            db.session.commit()
            return cs.OK, {'line_code': line_code}
        else:
            return cs.LOCATION_CODE_ERR, {'line_code': line_code}
    except:
        logger.error("modify line err : {}".format(traceback.format_exc(), ))
        raise
    finally:
        db.session.rollback()
