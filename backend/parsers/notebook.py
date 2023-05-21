from .common import process_file
from langchain.document_loaders import NotebookLoader
from fastapi import UploadFile


def process_ipnyb(vector_store, file: UploadFile, stats_db):
    return process_file(vector_store, file, NotebookLoader, "ipynb", stats_db=stats_db)
