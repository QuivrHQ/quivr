from .common import process_file
from langchain.document_loaders.epub import UnstructuredEPubLoader
from fastapi import UploadFile


def process_epub(file: UploadFile, enable_summarization):
    return process_file(file, UnstructuredEPubLoader, ".epub", enable_summarization)
