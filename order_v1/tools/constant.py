#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/14 14:32
# @Author  : Xsh
# @File    : constant.py
# @Software: PyCharm

import re

OK = 1000
DB_ERROR = 1001
AUTH_ERROR = 1002
SERVER_ERR = 1004
DATE_INTERVAL_TOO_LONG = 1009
AUTH_FAIL = 1100
TOKEN_INVALID = 1101
NO_USER_ = TOKEN_INVALID
NO_USER_EXIST = 1102
USER_OUT = 1103
USER_EXIST = 1104
REGISTER_ERR = 1105
USER_ACTIVE_ERROR = 1106
PASSWD_ERR = 1107
PARAMS_ERROR = 1303
PARAMS_TYPE_ERROR = 1304
VERIFYING_ERROR = 1305
NOT_CARGO_ORDER = 1402
CARGO_ORDER_STATUS_ABNORMAL = 1403
LOCATION_ERR = 1501
LOCATION_CODE_ERR = 1502
LOCATION_INFO_ERR = 1503
LINE_STATUS_ERR = 1504
LINE_TYPE_ERR = 1505
LINE_CODE_ERR = 1506
LINE_PUSH_ERR = 1507
NO_LINE_VOLUME = 1508
LINE_VOLUME_NOT_PENDING = 1509
PLATE_ERR = 1601
PLATE_EXIST = 1602
WAYBILL_NUMBER_ERR = 1701
WAYBILL_STATUS_ERR = 1702

ERR_MSG = {
    1000: '成功',
    1001: '服务器打了个盹',
    1002: '权限错误',
    1004: '服务器开小差',
    1005: '刷新回调',
    1009: '日期时间间隔过长',
    1100: '密码输入错误，请重新输入',
    1101: '您的帐号登录已过期失效，请重新登登录',
    1102: '该用户不存在',
    1103: '您的帐号已在其他手机登录',
    1104: '该手机已被注册',
    1105: '网络连接失败',
    1106: '用户未激活',
    1107: '原密码输入错误，请重新输入',
    1303: '参数错误',
    1304: '参数类型错误',
    1305: '验证码错误',
    1402: '货物订单不存在',
    1403: '货物订单状态异常',
    1501: '转运网点错误',
    1502: '转运网点编码错误',
    1503: '径停点信息错误',
    1504: '线路属性错误',
    1505: '线路状态错误',
    1506: '线路编码错误',
    1507: '推荐线路错误',
    1508: 'line_volume不存在',
    1509: '待处理货量为零',
    1601: '车牌错误',
    1602: '车牌已存在',
    1701: '运单编号不存在',
    1702: '运单状态错误'
}

USER_ROLE_TYPE = {
    7: u"线路规划专员",
    8: u"货物订单统筹专员",
    9: u"运单统筹专员",
    10: u"商家",
    11: u"承运商"
}
USER_ROLE_INFO = {
    u"线路规划专员": 7,
    u"货物订单统筹专员": 8,
    u"运单统筹专员": 9,
    u"商家": 10,
    u"承运商": 11
}

# 操作货物订单权限
ACTION_CARGO_ORDER_ROLE = [8, 9, 10, 11]
# 查看线路列表权限
SELECT_LINE_ROLE = [7, 8, 9]

ORDER_TYPE = {
    1: u"货物订单",
    2: u"车辆订单",
    3: u"运输订单"
}

ORDER_INFO = {
    u"货物订单": 1,
    u"车辆订单": 2,
    u"运输订单": 3
}

CARGO_ORDER_STATUS_INFO = {
    u"待接单": 200,
    u"已接单": 201,
    u"运输中": 300,
    u"异常运输": 400,
    u"已到达": 500,
    u"已作废": 501,
    u"已签收": 600
}

CARGO_ORDER_STATUS_INDEX = {
    200: u"待接单",
    201: u"已接单",
    300: u"运输中",
    400: u"异常运输",
    500: u"已到达",
    501: u"已作废",
    600: u"已签收"
}

CARGO_ORDER_STATUS_CHANGE = {
    200: [201, 501],
    201: [300, ],
    300: [400, 500],
    400: [500, ],
    500: [],
    501: []
}

WAYBILL_STATUS_CHANGE = {
    200: 300,
    300: 500
}

WAYBILL_CARGO_STATUS_CHANGE = {
    200: 201,
    300: 300,
    500: 500
}

ACTION_TYPE_INFO = {
    u"创建货物订单": 200,
    u"接单": 201,
    u"货物运输中": 300,
    u"运输异常": 400,
    u"货物订单到达": 500
}

ACTION_TYPE_INDEX = {
    200: u"创建货物订单",
    201: u"接单",
    300: u"货物运输中",
    400: u"运输异常",
    500: u"货物订单到达"
}
# 绑定用户角色和操作权限
USER_ROLE_ACTION = {
    8: [201, 500],
    9: [300, ],
    10: [200, ],
    11: []
}

CARGO_ORDER_TYPE_INFO = {
    u"正常": 1,
    u"注销": 2
}

CARGO_ORDER_TYPE_INDEX = {
    1: u"正常",
    2: u"注销"

}

SELECT_FLAG_INFO = {
    u"查询始发地订单": 1,
    u"查询目的地订单": 2
}

SELECT_FLAG_INDEX = {
    1: u"查询始发地订单",
    2: u"查询目的地订单"
}

LOCATION_STATUS_INFO = {
    u"启用": 1,
    u"禁用": 2
}

LOCATION_STATUS_INDEX = {
    1: u"启用",
    2: u"禁用"
}

LINE_STATUS_INFO = {
    u"启用": 1,
    u"禁用": 2
}

LINE_STATUS_INDEX = {
    1: u"启用",
    2: u"禁用"
}

TRUCK_STATUS_INFO = {
    u"启用": 1,
    u"禁用": 2
}

TRUCK_STATUS_INDEX = {
    1: u"启用",
    2: u"禁用"
}

LINE_LOCATION_STATUS_INFO = {
    u"启用": 1,
    u"禁用": 2
}

LINE_LOCATION_STATUS_INDEX = {
    1: u"启用",
    2: u"禁用"
}

LINE_TYPE_INFO = {
    u"临时": 1,
    u"正式": 2
}

LINE_TYPE_INDEX = {
    1: u"临时",
    2: u"正式"
}

WAYBILL_TYPE_INFO = {
    u"正常": 1,
    u"异常": 2,
    u"废止": 3
}

WAYBILL_TYPE_ORDER_STATUS = {
    1: 300,
    2: 400,
    3: 400
}


WAYBILL_TYPE_INDEX = {
    1: u"正常",
    2: u"异常",
    3: u"废止"
}

WAYBILL_STATUS_INFO = {
    u"待装车": 200,
    u"运输中": 300,
    u"已完成": 500
}

WAYBILL_STATUS_INDEX = {
    200: u"待装车",
    300: u"运输中",
    500: u"已完成"
}

IS_ONWAY_INFO = {
    u"在途": 1,
    u"到达": 2
}

IS_ONWAY_INDEX = {
    1: u"在途",
    2: u"到达"
}

LOGIN_EXPIRE = 2 * 3600

re_date = '^\d{4}(-)\d{2}(-)\d{2}$'


def is_date(date_value):
    """判断字符的格式是否为 1990-01-21 """
    if not date_value:
        return None
    else:
        if re.search(re_date, str(date_value)):
            return True
        else:
            return False


def is_chinese(uchar):
    """判断一个unicode是否是汉字"""
    if uchar >= u'\u4e00' and uchar <= u'\u9fa5':
        return True
    else:
        return False


def is_number(uchar):
    """判断一个unicode是否是数字"""
    if uchar >= u'\u0030' and uchar <= u'\u0039':
        return True
    else:
        return False


def is_alphabet(uchar):
    """判断一个unicode是否是英文字母"""
    if (uchar >= u'\u0041' and uchar <= u'\u005a') or (uchar >= u'\u0061' and uchar <= u'\u007a'):
        return True
    else:
        return False
