#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/8/15 18:48
# @Author  : 雷雨
# @File    : vector.py
# @Desc    :


class Qdrant:

    def __init__(self, collection_name, qdrant):
        self.qdrant = qdrant
        self.collection_name = collection_name

    @classmethod
    def create(cls):
        client = qdrant_client.QdrantClient(path=os.path.join(root_path, "db/Qdrant"), prefer_grpc=True)
        qdrant = Qdrant(
            client=client,
            collection_name=collection_name,
            embeddings=embeddings
        )
        return cls(collection_name, qdrant)

    @classmethod
    def save(cls, path, collection_name, docs: List[Document]):
        embeddings = OpenAIEmbeddings(openai_api_key=get_openai_key())
        qdrant = Qdrant.from_documents(
            docs, embeddings,
            path=os.path.join(root_path, db_location),
            collection_name=collection_name
        )
        return cls(path, collection_name)

    def search(self, query, collection_name, k: int = 4):
        embeddings.openai_api_key = get_openai_key()
        found_docs = self.qdrant.similarity_search_with_score(
            query,
            k=k
        )
        return found_docs