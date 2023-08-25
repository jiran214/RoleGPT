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
from complements.interaction import InteractionType
from complements.message import MessageQueue, Message
from complements import knowledge
from roles.base import Role
from tools import interaction


class Env:
    def __init__(self, role_map: Dict[str, Role]):
        self.role_map = role_map

    def publish(self, message: Message):
        message_queue_list = [role.message_queue for role in self.role_map.values() if role is not message.origin]
        for message_queue in message_queue_list:
            message_queue.put(message)

    def send_message(self, message: Message):
        message.to.message_queue.put(message)

    def send(self, message: Message):
        if message.interaction_type == InteractionType.dialog:
            self.send_message(message)
        elif message.interaction_type == InteractionType.conference:
            self.publish(message)



class Group:
    group_name: str = 'default_group'

    def __init__(self, Roles: List[Type[Role]], invest):
        self.Roles = Roles
        self.invest = invest
        self.roles: List[Role] = []
        self.init()

    def init(self):
        # 加载Env
        role_map = {
            Role.name: Role for Role in self.Roles
        }
        env = Env(role_map=role_map)
        # 全局配置
        interaction.dialog_role_map = {role: Role for role, Role in role_map.items() if Role.can_initiate_dialog}
        # 初始化角色
        for role_cls in self.Roles:
            common_tools = []
            if len(self.Roles) > 1 and interaction.dialog_role_map:
                # 加载公共工具
                common_tools.append(interaction.initialize_dialog_tool(role_cls))
            # 初始化角色
            role = role_cls.init(env, common_tools)
            # 加载公共知识库
            common_path = (config.knowledge_path / 'common')
            if len([path for path in common_path.iterdir()]) > 0:
                knowledge_base = knowledge.Knowledge(base_name=f"{self.group_name}.common")
                dir_path = common_path.absolute()
                knowledge_base.learn(dir_path)
                role.set_common_knowledge(knowledge_base)
            self.roles.append(role)

    def run(self):
        print('run')
        for role in self.roles:
            print(role.brain.functions)
            role.wait()
