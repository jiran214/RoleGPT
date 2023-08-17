#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/8/15 17:49
# @Author  : 雷雨
# @File    : role_context.py
# @Desc    :
from typing import Optional

from pydantic import BaseModel

from complements.memory import ShortTermMemory, LongTermMemory, MemoryFragment
from complements.knowledge import Knowledge
from modules.loader import Loader


class RoleContext(BaseModel):
    shor_term_memory: Optional[ShortTermMemory]
    long_term_memory: Optional[LongTermMemory]
    knowledge_base: Optional[Knowledge]

    def summary(self):
        """对短期或长期记忆总结"""
        pass