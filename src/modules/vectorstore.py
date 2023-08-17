#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/8/15 18:48
# @Author  : 雷雨
# @File    : vectorstore.py
# @Desc    :
import abc

from langchain.vectorstores import VectorStore, Qdrant
from qdrant_client import QdrantClient


from modules import llm


class BaseVS(abc.ABC, VectorStore):

    @classmethod
    @abc.abstractmethod
    def from_disk(cls, collection):
        ...

    @classmethod
    @abc.abstractmethod
    def from_memory(cls, collection):
        ...


class QdrantVS(Qdrant, BaseVS):
    @classmethod
    def from_disk(cls, collection: str):
        client = QdrantClient(path="path/to/db")  # Persists changes to disk
        qdrant = cls(
            client=client,
            collection_name=collection,
            embeddings=llm.embeddings,
        )
        return qdrant

    @classmethod
    def from_memory(cls, collection: str):
        client = QdrantClient(":memory:")
        qdrant = cls(
            client=client,
            collection_name=collection,
            embeddings=llm.embeddings,
        )
        return qdrant
