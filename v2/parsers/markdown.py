from .common import process_file
from langchain.document_loaders import UnstructuredMarkdownLoader
from fastapi import UploadFile

def process_markdown(vector_store, file: UploadFile, stats_db):
    return process_file(vector_store, file, UnstructuredMarkdownLoader, ".md", stats_db=stats_db)
