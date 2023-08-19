#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/8/15 18:48
# @Author  : 雷雨
# @File    : vectorstore.py
# @Desc    :
import abc

from langchain.vectorstores import Qdrant
from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, Distance
from config import root_path
from modules import llm
from complements import memory


class MemoryFactory:
    _client = {}

    @classmethod
    def get_client(cls, path):
        if path not in cls._client:
            client = QdrantClient(path=path)
            cls._client[path] = client
        return cls._client[path]

    @classmethod
    def from_disk(cls, collection: str):
        path = str(root_path / 'db')
        client = cls.get_client(path=path)
        collections = client._client.collections.keys()
        if not (collection in collections):
            print(f"新 collection {collection}")
            client.recreate_collection(
                **{'collection_name': collection,
                 'vectors_config': VectorParams(
                     size=1536, distance=Distance.COSINE, hnsw_config=None, quantization_config=None, on_disk=True
                 ),
                 'shard_number': None,
                 'replication_factor': None,
                 'write_consistency_factor': None,
                 'on_disk_payload': None,
                 'hnsw_config': None,
                 'optimizers_config': None,
                 'wal_config': None, 'quantization_config': None,
                 'init_from': None, 'timeout': None}
            )
        qdrant = Qdrant(
            client=client,
            collection_name=collection,
            embeddings=llm.Embedding,
        )

        return memory.LongTermMemory(qdrant)

    @classmethod
    def from_memory(cls, collection: str):
        qdrant = Qdrant(
            client=cls.get_client(":memory:"),
            collection_name=collection,
            embeddings=llm.Embedding,
        )
        return memory.ShortTermMemory(qdrant)
