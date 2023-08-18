import os
from pathlib import Path
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

    def __init__(self, dir_path: Path):
        self.dir_path = dir_path
        self.file_path_list: List[Path] = []

    def load_pdf(self, path) -> List[Document]:
        loader = PyPDFLoader(path)
        pages = loader.load_and_split(text_splitter=pdf_splitter)
        return pages

    def load_txt(self, path) -> List[Document]:
        loader = TextLoader(path, encoding='utf-8')
        documents = loader.load()
        docs = text_splitter.split_documents(documents)
        return docs

    def is_new_file(self):
        self.file_path_list = [path for path in self.dir_path.iterdir()]
        if self.file_path_list:
            return True
        else:
            print('no new file')

    def load(self):
        for path in self.file_path_list:
            file_extension = path.suffix.strip('.')
            load_func = getattr(self, f'load_{file_extension}', None)
            if load_func:
                yield load_func(path)
            else:
                print(f'暂时不支持该类型文件:{path}')
