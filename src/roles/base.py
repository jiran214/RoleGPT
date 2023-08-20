#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/8/15 17:51
# @Author  : 雷雨
# @File    : base.py
# @Desc    :
import abc
from typing import List, Type

from langchain import LLMChain, BasePromptTemplate, PromptTemplate
from langchain.agents import AgentExecutor
from langchain.chains.base import Chain

import config
from complements import memory, knowledge
from complements.converters.base import Converter
from complements.knowledge import Knowledge
from complements.message import MessageQueue, Message
from modules import llm
from modules.agent import initialize_role_agent
from modules.vectorstore import MemoryFactory
from src.complements.role_context import RoleContext
from tools.base import ToolModel


class Role(abc.ABC):
    name = None
    prompt: BasePromptTemplate = None
    tools: List[Type[ToolModel]] = []
    output_converters: List[Converter] = []

    def __init__(self, role_context, message_queue, brain: Chain):
        self.role_context: 'RoleContext' = role_context
        self.message_queue: MessageQueue = message_queue
        self.brain = brain

    def validate(self):
        assert self.name is not None, 'name未定义，请声明变量name'
        assert self.prompt is not None, 'prompt未定义，请声明变量prompt'

    @abc.abstractmethod
    def react(self, message: Message):
        """使用llm思考，中途可能会暂停"""
        prompt = """"""
        llm_resp = self.brain.run('123')
        return llm_resp

    def wait(self):
        # self.validate()
        for message in self.message_queue.get():
            data = self.react(message)
            # 异步
            for converter in self.output_converters:
                converter.convert(data)
            return data

    @classmethod
    def init(cls):
        if cls.tools:
            brain = initialize_role_agent(tools=cls.tools, prompt=cls.prompt)
        else:
            brain = LLMChain(
                llm=llm.ChatGPT,
                prompt=PromptTemplate.from_template(cls.prompt)
            )
        knowledge_base = knowledge.Knowledge(base_name=f"{cls.name}.long_term_memory")
        dir_path = (config.knowledge_path / cls.name).absolute()
        knowledge_base.learn(dir_path)
        role_context = RoleContext(
            shor_term_memory=MemoryFactory.from_memory(f"{cls.name}.short_term_memory"),
            long_term_memory=knowledge_base.as_long_term_memory(),
            knowledge_base=None
        )
        return cls(role_context, MessageQueue(), brain)

    def set_common_knowledge(self, knowledge_base: Knowledge):
        self.role_context.knowledge_base = knowledge_base


class Engineer(Role):
    ...