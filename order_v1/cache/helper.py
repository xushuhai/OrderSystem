#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/14 14:15
# @Author  : Xsh
# @File    : helper.py
# @Software: PyCharm

import redis

from config.test import EXPIRE_TIME, REDIS_PUB_URL, REDIS_URL

r = redis.from_url(REDIS_URL)
r_pub = redis.from_url(REDIS_PUB_URL)



def rset(key, value):
    r.set(key, value)


def hmset(key, value):
    '''

    :param key: redis.hmset key
    :param value: redis.hmset field&vlaue
                  value_example:{'device_id': device_id}
    :return:
    '''
    r.hmset(key, value)
    r.expire(key, EXPIRE_TIME)

















from log.info import logger
from tools import constant as cs
from flask import session
from cache.keys import get_token

def deco_hgetall(func):
    def wrapper(*args, **kwargs):
        try:
            val = r.hgetall(get_token(kwargs['key']))
            logger.debug('val is {}'.format(val))
            if val:
                for key in val:
                    val[key] = val[key].decode(encoding='UTF-8', errors='strict')
                logger.debug('key = {} value = {} in cache'.format(get_token(kwargs['key']), val))
                return None, val
            val = func(*args, **kwargs)
            if val[1]:
                logger.debug('key = {} value = {} in db'.format(kwargs['key'], val[1]))
                r.hmset((get_token(kwargs['key'])), val[1])
                logger.debug('key = {} login_expire = {}'.format(get_token(kwargs['key']), cs.LOGIN_EXPIRE))
                rexpire(get_token(kwargs['key']), cs.LOGIN_EXPIRE)
            return val
        except:
            raise

    return wrapper


def rset(key, value):
    r.set(key, value)


def hmset(key, value):
    '''

    :param key: redis.hmset key
    :param value: redis.hmset field&vlaue
                  value_example:{'device_id': device_id}
    :return:
    '''
    r.hmset(key, value)
    r.expire(key, EXPIRE_TIME)


def delete(key):
    r.delete(key)


def rget(key):
    return r.get(key)


def hgetall(key):
    return r.hgetall(key)


def hget(key, value):
    return r.hget(key, value)


def hset(key, value, data):
    return r.hset(key, value, data)


def deco_update(func):
    def wrapper(*args, **kwargs):
        val = func(*args, **kwargs)
        n_val = val[1]
        if not n_val:
            return val
        o_val = r.hgetall(kwargs['key'])
        if o_val:
            for k in o_val:
                if k in n_val and n_val[k] and o_val[k] != n_val[k]:
                    o_val[k] = n_val[k]
                r.hmset(kwargs['key'], o_val)
            return None, n_val
        return wrapper


# 将一个值或多个值插入列表头部
def lpush(key, value):
    r_pub.lpush(key, value)


# 将一个值或多个值插入列表尾部
def rpush(key, value):
    r.rpush(key, value)


# 移除列表第一个元素
def lpop(key):
    return r_pub.lpop(key)


# 移除列表最后一个元素
def blpop(key):
    return r.blpop(key)


# 将 key 中储存的数字值增一
def incr(key):
    return r.incr(key)


# 设置 key 的过期时间。key 过期后将不再可用
def rexpire(key, value):
    r.expire(key, value)


# 将信息发送到指定的频道
def rpublish(key, value):
    r.publish(key, value)
