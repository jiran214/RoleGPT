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
import prompts

class RoleContext(BaseModel):
    shor_term_memory: Optional[ShortTermMemory]
    long_term_memory: Optional[LongTermMemory]
    knowledge_base: Optional[Knowledge]

    def summary(self):
        """对短期或长期记忆总结"""
        pass

    def get_memory(self, cue):
        short_term_memory = self.long_term_memory.recall(cue)
        long_term_memory = self.shor_term_memory.recall(cue)
        prompt = prompts.core_v1.MEMORY.format(
            short_term_memory=short_term_memory,
            long_term_memory=long_term_memory
        )
        return prompt

    class Config:
        arbitrary_types_allowed = True
