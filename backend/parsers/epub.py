from .common import process_file
from langchain.document_loaders.epub import UnstructuredEPubLoader
from fastapi import UploadFile


def process_epub(vector_store, file: UploadFile, stats_db):
    return process_file(vector_store, file, UnstructuredEPubLoader, ".epub", stats_db=stats_db)
