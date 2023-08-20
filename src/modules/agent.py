#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/8/15 18:47
# @Author  : 雷雨
# @File    : agent.py
# @Desc    :
from typing import List, Type, Optional

from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent
from langchain.schema import SystemMessage

import config
from modules import llm
from tools.base import LangchainToolAdapter, ToolModel


def initialize_role_agent(
        tools: List[Type[ToolModel]],
        prompt: Optional[SystemMessage] = SystemMessage(
            content="You are a helpful AI assistant."
        ),
        agent=AgentType.OPENAI_FUNCTIONS
):
    agent = initialize_agent(
        [LangchainToolAdapter.from_tool_model(tool) for tool in tools],
        llm=llm.ChatGPT0613,
        agent=agent,
        agent_kwargs={'system_message': prompt}
    )
    return agent
