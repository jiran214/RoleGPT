#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/8/15 17:51
# @Author  : 雷雨
# @File    : base.py
# @Desc    :
from src.complement.role_context import RoleContext


class Role:
    tools = None
    role_context: 'RoleContext' = None
    brain = None
    prompt = None


class Engineer(Role):
    ...