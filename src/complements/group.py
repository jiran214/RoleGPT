#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/8/16 16:34
# @Author  : 雷雨
# @File    : group.py
# @Desc    :
import abc
from copy import deepcopy
from typing import List, Dict, Type

import config
from complements.message import MessageQueue, Message
from complements import knowledge
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


class Group:

    group_name: str = 'default_group'

    def __init__(self, Roles: List[Type[Role]], invest):
        self.Roles = Roles
        self.invest = invest
        self.roles: List[Role] = []
        self.init()

    def init(self):
        # 初始化角色
        for role_cls in self.Roles:
            role = role_cls.init()
            knowledge_base = knowledge.Knowledge(base_name=f"{self.group_name}:common")
            dir_path = (config.knowledge_path / 'common').absolute()
            knowledge_base.learn(dir_path)
            role.set_common_knowledge(knowledge_base)
            self.roles.append(role)

    def run(self):
        for role in self.roles:
            role.wait()