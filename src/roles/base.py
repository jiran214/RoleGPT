#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/8/15 17:51
# @Author  : 雷雨
# @File    : base.py
# @Desc    :
import abc
from typing import List

from langchain.agents import AgentExecutor

import config
from complements import memory, knowledge
from complements.converters.base import Converter
from complements.knowledge import Knowledge
from complements.message import MessageQueue, Message
from modules.vectorstore import MemoryFactory
from src.complements.role_context import RoleContext


class Role(abc.ABC):
    name = None
    tools = None
    brain: AgentExecutor = None
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
        """使用llm思考，中途可能会暂停"""
        prompt = """"""
        llm_resp = ""
        return llm_resp

    def wait(self):
        # self.validate()
        print('run')
        print(self.role_context.long_term_memory.recall('123'))
        for message in self.message_queue.get():
            data = self.react(message)
            # 异步
            for converter in self.output_converters:
                converter.convert(data)
            return data

    @classmethod
    def init(cls):
        knowledge_base = knowledge.Knowledge(base_name=f"{cls.name}.long_term_memory")
        dir_path = (config.knowledge_path / cls.name).absolute()
        knowledge_base.learn(dir_path)
        role_context = RoleContext(
            shor_term_memory=MemoryFactory.from_memory(f"{cls.name}.short_term_memory"),
            long_term_memory=knowledge_base.as_long_term_memory(),
            knowledge_base=None
        )
        return cls(role_context, MessageQueue())

    def set_common_knowledge(self, knowledge_base: Knowledge):
        self.role_context.knowledge_base = knowledge_base


class Engineer(Role):
    ...