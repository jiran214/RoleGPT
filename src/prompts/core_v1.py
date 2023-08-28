#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/8/25 10:23
# @Author  : 雷雨
# @File    : core_v1.py
# @Desc    :
# 外部变量：对话/会议、短时记忆、长期记忆、知识库、指令、输出语言
from langchain.agents.react.base import DocstoreExplorer

SYSTEM = """{profile}"""

PROMPT = """## 你的记忆
{memory}
## 查询知识库获取的信息
{knowledge}
## {interaction_type}
{interaction_message}

请对{interaction_type}做出回应,语言为{language}"""

MEMORY = """### 短期记忆
{short_term_memory}
### 长期记忆
{long_term_memory}"""