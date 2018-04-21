#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/14 15:35
# @Author  : Xsh
# @File    : auth.py
# @Software: PyCharm

import re
import hashlib
import random
import json
import datetime
import traceback
from celery import Celery

from model.user import User
from config.order_app import db
from tools import constant as cs
from cache.helper import deco_hgetall, rset, rexpire, rget
from cache.keys import get_sms
from log.info import logger
from config.test import SIGN_NAME, TEMPLATE_CODE, CELERY_ROUTE_CREATE, QUEUE, SMS_EXPIRE_TIME

celery = Celery()
celery.config_from_object('celeryconfig')



def get_verifying_code(telephone):
    """
    根据手机号码发送验证码
    :param telephone:
    :return:cs.OK
    """
    verifying_telephone = r'^1[34578]\d{9}'
    result = re.findall(verifying_telephone, telephone)
    if result:
        my_str = ''
        for i in range(6):
            my_str += str(random.randint(0, 9))
        params = dict(code=my_str)
        params = json.dumps(params)
        celery.send_task(CELERY_ROUTE_CREATE,
                         args=[telephone, SIGN_NAME, TEMPLATE_CODE, params], queue=QUEUE)
        # 将验证码插入redis中,并设置销毁时间
        try:
            rset(get_sms(telephone), my_str)
            rexpire(get_sms(telephone), SMS_EXPIRE_TIME)
        except:
            logger.error('insert verifying code in redis err:{}'.format(traceback.format_exc(), ))
            raise
        return cs.OK, my_str
    else:
        return cs.PARAMS_ERROR, None



def register_user(verifying_code, telephone, name, username, password, mobile, role_type, fk_location_code, fk_plate):
    """
    注册
    :param verifying_code:
    :param telephone:
    :param name:
    :param username:
    :param password:
    :param mobile:
    :param role_type:
    :param fk_location_code:
    :param fk_plate:
    :return: cs.OK
    """
    verifying = rget(get_sms(telephone))
    if not verifying or verifying != verifying_code:
        return cs.VERIFYING_ERROR, None
    user = User.query.filter_by(username=username).first()
    if user:
        return cs.USER_EXIST, None
    print role_type
    print cs.USER_ROLE_TYPE.keys()
    if int(role_type) not in cs.USER_ROLE_TYPE.keys():
        return cs.AUTH_ERROR, None
    if int(role_type) in [cs.USER_ROLE_INFO[u"承运商"], cs.USER_ROLE_INFO[u"商家"]]:
        fk_location_code = None
    m2 = hashlib.md5()
    m2.update(password)
    password = m2.hexdigest()
    try:
        user = User(name, username, password, mobile, role_type, fk_location_code, fk_plate)
        db.session.add(user)
        db.session.commit()
        return cs.OK, None
    except:
        logger.error('register user error:{}'.format(traceback.format_exc(), ))
        raise
    finally:
        db.session.remove()



@deco_hgetall
def get_user(username, password, key):
    """
    登录
    :param username:
    :param password:
    :param key:
    :return:
    """
    user = User.query.filter_by(username=username).first()
    if not user:
        return cs.NO_USER_EXIST, None
    if not user.role_type in cs.USER_ROLE_TYPE.keys():
        return cs.AUTH_ERROR, None
    m2 = hashlib.md5()
    m2.update(password)
    if user.password == m2.hexdigest():
        user_dict = user.to_dict()
        expire_time = datetime.date.today() + datetime.timedelta(cs.LOGIN_EXPIRE)
        user_dict['expire_time'] = expire_time.strftime("%Y-%m-%d %H:%M:%S")
        user_dict['token'] = key
        db.session.remove()
        return None, user_dict
    else:
        db.session.remove()
        return cs.AUTH_FAIL, None


def modify_password(username, old_password, new_password):
    """
    修改密码
    :param username:
    :param old_password:
    :param new_password:
    :return:cs.OK
    """
    user = User.query.filter_by(username=username).first()
    m2 = hashlib.md5()
    m2.update(old_password)
    if user.password == m2.hexdigest():
        try:
            m3 = hashlib.md5()
            m3.update(new_password)
            user.password = m3.hexdigest()
            db.session.commit()
            return cs.OK, None
        except:
            logger.error('modify password error:{}'.format(traceback.format_exc(), ))
            raise
        finally:
            db.session.remove()
    else:
        return cs.PASSWD_ERR, None


def reset_password(username, new_password, verifying_code):
    """
    短信找回密码
    :param username:
    :param new_password:
    :param verifying_code:
    :return:cs.OK
    """
    verifying = rget(get_sms(username))
    if not verifying or verifying != verifying_code:
        return cs.VERIFYING_ERROR, None
    user = User.query.filter_by(username=username).first()
    if user:
        try:
            m2 = hashlib.md5()
            m2.update(new_password)
            user.password = m2.hexdigest()
            db.session.commit()
            return cs.OK, None
        except:
            logger.error('reset password err:{}'.format(traceback.format_exc(), ))
            raise
        finally:
            db.session.remove()
    else:
        return cs.NO_USER_EXIST, None


def get_user_username(user_id):
    """

    :param user_id:
    :return:username
    """
    user_obj = User.query.filter_by(id=user_id).first()
    if user_obj:
        return user_obj.username
