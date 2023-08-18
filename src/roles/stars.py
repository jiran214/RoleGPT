#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/8/18 16:02
# @Author  : 雷雨
# @File    : stars.py
# @Desc    :
from complements.message import Message
from roles.base import Role


class KanyeWest(Role):
    name = 'Kanye West'
    tools = None
    brain = None
    prompt = None
    output_converters = []

    def react(self, message: Message):
        pass
