#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/8/15 18:48
# @Author  : 雷雨
# @File    : vectorstore.py
# @Desc    :
import abc

from langchain.vectorstores import VectorStore, Qdrant
from qdrant_client import QdrantClient

from config import root_path
from modules import llm


class VSCreateMixin:

    __client = {}

    @classmethod
    def get_client(cls, path):
        if path not in cls.__client:
            cls.__client[path] = QdrantClient(path)
        return cls.__client[path]

    @classmethod
    @abc.abstractmethod
    def from_disk(cls, collection):
        ...

    @classmethod
    @abc.abstractmethod
    def from_memory(cls, collection):
        ...


class QdrantVS(Qdrant, VSCreateMixin):

    @classmethod
    def from_disk(cls, collection: str):
        qdrant = cls(
            client=cls.get_client(path=str(root_path / 'db')),
            collection_name=collection,
            embeddings=llm.Embedding,
        )
        return qdrant

    @classmethod
    def from_memory(cls, collection: str):
        qdrant = cls(
            client=cls.get_client(":memory:"),
            collection_name=collection,
            embeddings=llm.Embedding,
        )
        return qdrant
