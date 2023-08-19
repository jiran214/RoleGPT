#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/8/16 18:31
# @Author  : 雷雨
# @File    : main.py
# @Desc    :
import config
import roles.stars
from complements.group import Group


Group(
    Roles=[roles.stars.KanyeWest],
    invest=100
).run()