#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/8/15 17:51
# @Author  : 雷雨
# @File    : base.py
# @Desc    :
import abc
from typing import List

from complement.converters.base import Converter
from complement.message import MessageQueue, Message
from src.complement.role_context import RoleContext


class Role(abc.ABC):
    name = None
    tools = None
    brain = None
    prompt = None
    output_converters: List[Converter] = []

    def __init__(self, role_context, message_queue):
        self.role_context: 'RoleContext' = role_context
        self.message_queue: MessageQueue = message_queue

    def validate(self):
        assert self.name is not None, 'name未定义，请声明变量name'
        assert self.tools is not None, 'tools未定义，请声明变量tools'
        assert self.brain is not None, 'brain未定义，请声明变量brain'
        assert self.prompt is not None, 'prompt未定义，请声明变量prompt'

    @abc.abstractmethod
    def react(self, message: Message):
        llm_resp = self.think(message.message)
        res = ''
        return res

    @abc.abstractmethod
    def think(self, data):
        """使用llm思考，中途可能会暂停"""
        prompt = """"""
        llm_resp = ""
        return llm_resp

    def wait(self):
        self.validate()
        for message in self.message_queue.get():
            data = self.react(message)
            # 异步
            for converter in self.output_converters:
                converter.convert(data)
            return data


class Engineer(Role):
    ...