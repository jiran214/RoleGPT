#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/8/15 17:48
# @Author  : 雷雨
# @File    : memory.py
# @Des
import abc
from typing import List

from langchain.schema import Document
from langchain.vectorstores import Qdrant, VectorStore
from pydantic import BaseModel


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


class Memory:

    def __init__(self, client: VectorStore):
        self.client = client

    def recall(self, cue: MemoryCue):
        docs = self.client.similarity_search(query, k=4)
        return docs

    def memorize(self, fragment: List[MemoryFragment]):
        self.client.add_documents(fragment)


class ShortTermMemory(Memory):
    pass


class LongTermMemory(Memory):
    pass
