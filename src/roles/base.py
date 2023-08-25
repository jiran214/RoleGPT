#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/8/15 17:51
# @Author  : 雷雨
# @File    : base.py
# @Desc    :
import abc
from typing import List, Type, Optional

from langchain import LLMChain, BasePromptTemplate, PromptTemplate
from langchain.agents import AgentExecutor
from langchain.chains.base import Chain
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.schema import SystemMessage

import config
import prompts.core_v1
from complements import memory, knowledge
from complements.converters.base import Converter
from complements.group import Env
from complements.knowledge import Knowledge
from complements.message import MessageQueue, Message
from modules import llm
from modules.agent import initialize_role_agent
from modules.vectorstore import MemoryFactory
from src.complements.role_context import RoleContext
from tools.base import ToolModel


class Role(abc.ABC):
    name = None
    profile: BasePromptTemplate = None
    tools: List[Type[ToolModel]] = []
    output_converters: List[Converter] = []
    can_initiate_dialog = True

    def __init__(self, role_context, message_queue, env):
        self.role_context: 'RoleContext' = role_context
        self.message_queue: MessageQueue = message_queue
        self.env: Env = env
        self.brain: Optional[Chain] = None

    def validate(self):
        assert self.name is not None, 'name未定义，请声明变量name'
        assert self.profile is not None, 'profile未定义，请声明变量profile'

    def react(self, message: Message):
        """使用llm思考，中途可能会暂停"""
        cue = message.message
        prompt = prompts.core_v1.PROMPT.format(
            memory=self.role_context.get_memory(cue),
            knowledge=knowledge,
            interaction_type=message.interaction_type,
            interaction_message=message.message,
            language=config.language
        )
        llm_resp = self.brain.run(prompt)
        return llm_resp

    def wait(self):
        # self.validate()
        for message in self.message_queue.get():
            data = self.react(message)
            for converter in self.output_converters:
                converter.convert(data)
            return data

    def create_system_message(self) -> SystemMessage:
        return SystemMessage(content=prompts.core_v1.SYSTEM(self.profile))

    @classmethod
    def init(cls, env, common_tools: Optional[List[Type[ToolModel]]] = None):
        if common_tools: cls.tools.extend(common_tools)
        knowledge_base = knowledge.Knowledge(base_name=f"{cls.name}.long_term_memory")
        dir_path = (config.knowledge_path / cls.name).absolute()
        knowledge_base.learn(dir_path)
        role_context = RoleContext(
            shor_term_memory=MemoryFactory.from_memory(f"{cls.name}.short_term_memory"),
            long_term_memory=knowledge_base.as_long_term_memory(),
            knowledge_base=None
        )
        role = cls(role_context, MessageQueue(), env)
        role.set_brain()
        return role

    def set_common_knowledge(self, knowledge_base: Knowledge):
        self.role_context.knowledge_base = knowledge_base

    def set_brain(self):
        prompt = self.create_system_message()
        if self.tools:
            self.brain = initialize_role_agent(self, tools=self.tools, prompt=prompt)
        else:
            prompt = ChatPromptTemplate.from_messages([prompt])
            self.brain = LLMChain(
                llm=llm.ChatGPT,
                prompt=prompt
            )

class Engineer(Role):
    ...
