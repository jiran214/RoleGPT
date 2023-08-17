#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/8/16 16:34
# @Author  : 雷雨
# @File    : group.py
# @Desc    :
import abc
from copy import deepcopy
from typing import List, Dict

from complement.message import MessageQueue, Message
from complement import knowledge
from roles.base import Role


class Env:
    def __init__(self, knowledge_base, roles: Dict[str, Role]):
        self.knowledge_base: knowledge
        self.role_map = {}

    def publish(self, message: Message):
        message_queue_list = [role.message_queue for role in self.roles if role is not message.origin]
        for message_queue in message_queue_list:
            message_queue.put(message)

    def send_message(self, message: Message):
        Message.to.message_queue.put(message)


class BaseGroup(abc.ABC):
    roles = []

    def __init__(self):
        self.init()

    @abc.abstractmethod
    def init(self):
        # 初始化角色
        # 每个角色读取记忆
        # 每个角色加载记忆
        # 本地知识库加载知识
        pass

    @abc.abstractmethod
    def run(self):
        ...