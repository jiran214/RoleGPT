import os
from typing import List

from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader, PyPDFLoader
from langchain.vectorstores import Qdrant


db_location = "db/Qdrant"
docs_location = "static/documents/{}"

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=0,
    separators=["\n", "。", " ", ""],
    length_function=len
)

pdf_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100,
    separators=["\n\n", "\n", "。", " ", ""],
    length_function=len
)


class Loader:

    def __init__(self, dir_path):
        file_name = dir_path
        self.dir_path = dir_path
        self.file_name = file_name
        self.file_extension = file_name.split(".")[-1]

    def load_pdf(self, path) -> List[Document]:
        loader = PyPDFLoader(path)
        pages = loader.load_and_split(text_splitter=pdf_splitter)
        return pages

    def load_txt(self, path) -> List[Document]:
        loader = TextLoader(path, encoding='utf-8')
        documents = loader.load()
        docs = text_splitter.split_documents(documents)
        return docs

    def load(self):
        for path in self.dir_path:
            load_func = getattr(self, f'load_{self.file_extension}', None)
            if load_func:
                yield load_func(path)
            else:
                print('暂时不支持该类型文件')
