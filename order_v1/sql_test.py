#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/11 13:33
# @Author  : Xsh
# @File    : sql_test.py
# @Software: PyCharm

from models.graduation_project import GraduationProject

page_index = 1
page_size = 10
pg_items = GraduationProject.query(GraduationProject.subject_name).filter().paginate(int(page_index), int(page_size),
                                                                                    False)
pg_objs = pg_items.items
for pg_obj in pg_objs:
    print pg_obj
