#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/8/15 17:46
# @Author  : 雷雨
# @File    : config.py
# @Desc    :
from pathlib import Path
from langchain.agents import AgentType


root_path = Path(__file__).parent
knowledge_path = root_path.parent / 'knowledge'
agent_type = AgentType.OPENAI_FUNCTIONS
api_key = ''
api_key_list = [
    '',
]
language = '中文'
proxy = 'http://127.0.0.1:7890'

from utils import init
