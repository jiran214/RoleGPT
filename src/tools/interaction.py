#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/8/16 17:44
# @Author  : 雷雨
# @File    : interaction.py
# @Desc    :
from enum import Enum
from typing import Type

from pydantic import Field

from complements.interaction import InteractionType
from complements.message import Message
from roles.base import Role
from tools.base import ToolModel

# 全局拥有对话能力的role
dialog_role_map = {}


class InteractionTool(ToolModel):
    origin: str
    to: str
    message: str

    def use(self, role: Role):
        assert self.origin
        assert self.to
        message = Message(
            origin=dialog_role_map[self.origin],
            to=dialog_role_map[self.to],
            message=self.message,
        )
        role.env.send(message)

    @classmethod
    def schema(cls, *args, **kwargs):
        assert dialog_role_map, '未初始化dialog_role_map，不能使用该tool'
        return cls.schema()


def initialize_dialog_tool(role: Type[Role]) -> Type[InteractionTool]:
    role_list = list(dialog_role_map.keys())
    role_list.pop(role.name)

    class DialogTool(InteractionTool):
        origin: str = role.name
        to: str = Field(description='Whom you communicate with', enum=[])
        message: str = Field(description='Whom you communicate with Exchange dialogue content')
        interaction_type: str = InteractionType.dialog

        class Meta:
            name = "Dialog tool"
            description = "You can use this tool to initiate a conversation with a role."

    return DialogTool


def initialize_conference_tool(role: Type[Role]) -> Type[InteractionTool]:
    role_list = list(dialog_role_map.keys())
    role_list.pop(role.name)

    class ConferenceTool(InteractionTool):
        origin: str = role.name
        to: str = 'all'
        message: str = Field(description='Whom you communicate with other')
        interaction_type: str = InteractionType.conference

        class Meta:
            name = "Conference tool"
            description = "You can use this tool to held a meeting to inform everyone of the message."

    return ConferenceTool
