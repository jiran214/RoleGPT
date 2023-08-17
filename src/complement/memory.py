#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/8/15 17:48
# @Author  : 雷雨
# @File    : memory.py
# @Des
import abc
from typing import List

from langchain.schema import Document
from pydantic import BaseModel

from modules import BaseVS, VS


class MemoryFragment(Document):
    """处理metadata"""
    @classmethod
    def from_docs(cls, docs: List[Document]):
        return [
            cls(
                page_content=doc.page_content,
                metadata=doc.metadata
            ) for doc in docs
        ]


class MemoryCue(BaseModel):
    """通过该model查询向量数据库"""
    ...


class BaseMemory(abc.ABC):
    def __init__(self, collection):
        self.vs: BaseVS = VS(collection)

    @abc.abstractmethod
    def recall(self, cue: MemoryCue):
        ...

    @abc.abstractmethod
    def memorize(self, fragment: List[MemoryFragment]):
        ...


class ShortTermMemory(BaseMemory):

    def recall(self, cue: MemoryCue):
        pass

    def memorize(self, fragment: List[MemoryFragment]):
        pass


class LongTermMemory(BaseMemory):
    def recall(self, cue: MemoryCue):
        pass

    def memorize(self, fragment: List[MemoryFragment]):
        pass