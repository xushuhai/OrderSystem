#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/21 15:45
# @Author  : Xsh
# @File    : inster_location.py
# @Software: PyCharm


import xlrd
import MySQLdb
import datetime
import logging
import sys
import random

# db
conn = MySQLdb.connect(
    host='localhost',
    port=3306,
    user='root',
    passwd='123456',
    db='order_system',
)
cur = conn.cursor()

conn.set_character_set('utf8')
cur.execute('SET NAMES utf8;')
cur.execute('SET CHARACTER SET utf8;')
cur.execute('SET character_set_connection=utf8;')

# logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%y-%m-%d %H:%M:%S',
                    filename='logger.log',
                    filemode='a')
# 定义一个Handler打印INFO及以上级别的日志到sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# 设置日志打印格式
formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
console.setFormatter(formatter)
# 将定义好的console日志handler添加到root logger
logging.getLogger('').addHandler(console)


def read_excel(filename):
    # 打开文件
    workbook = xlrd.open_workbook(filename)
    # 获取Sheet1
    sheet1_name = workbook.sheet_names()[0]
    # 根据sheet索引获取sheet内容
    sheet1 = workbook.sheet_by_name(sheet1_name)
    flag = ['location_name', 'location_code', 'lot', 'lat', 'detailed_address', 'province', 'city']
    order_datas = []
    for i in range(1, sheet1.nrows):
        rows = sheet1.row_values(i)
        order_data = {}
        for j in range(sheet1.ncols):
            value = sheet1.cell_value(i, j)
            if isinstance(value, unicode):
                order_data[flag[j]] = value.strip(' ')
        if len(order_data) == 7:
            order_datas.append(order_data)

    return order_datas


def modify_order_data(datas):
    try:
        number = 0
        for data in datas:
            try:
                # insert data
                sql = "INSERT INTO location(location_name, location_code, detailed_address, lot, lat, province, city, create_time, update_time) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                param = (data['location_name'], data['location_code'], data['detailed_address'], data['lot'],
                         data['lat'], data['province'], data['city'], datetime.datetime.now(),
                         datetime.datetime.now())
                cur.execute(sql, param)

            except Exception, e:
                logging.error('sql err content:{}'.format(e))
                raise
    except Exception, e:
        logging.error('db err content:{}', format(e))
        raise
    finally:
        # 关闭游标
        cur.close()
        # 提交数据
        conn.commit()
        # 关闭数据库连接
        conn.close()


def start(filename):
    datas = read_excel(filename)
    modify_order_data(datas)
    print datas


if __name__ == '__main__':
    start(sys.argv[1])
