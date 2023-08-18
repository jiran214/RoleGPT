#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/8/15 17:48
# @Author  : 雷雨
# @File    : knowledge.py
# @Desc    :
from typing import List

from complements.memory import LongTermMemory, MemoryCue, MemoryFragment
from modules.loader import Loader


class Knowledge:

    def __init__(self, base_name):
        self.long_term_memory = LongTermMemory.from_disk(collection=base_name)

    def save(self, fragment: List[MemoryFragment]):
        self.long_term_memory.memorize(fragment)

    def search(self, cue: MemoryCue):
        self.long_term_memory.recall(cue)

    def learn(self, dir_path):
        loader = Loader(dir_path)
        if loader.is_new_file():
            for docs in loader.load():
                fragments = MemoryFragment.from_docs(docs)
                self.long_term_memory.memorize(fragments)

    def as_long_term_memory(self):
        return self.long_term_memory
