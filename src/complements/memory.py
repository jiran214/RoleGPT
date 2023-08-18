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

from modules import VS


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


class MemoryMethodMixin:

    def recall(self, cue: MemoryCue):
        query = ''
        docs = self.similarity_search(query, k=4)
        return docs

    def memorize(self, fragment: List[MemoryFragment]):
        self.add_documents(fragment)


class ShortTermMemory(VS, MemoryMethodMixin):
    pass


class LongTermMemory(VS, MemoryMethodMixin):
    pass