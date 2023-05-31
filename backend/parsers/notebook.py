from fastapi import UploadFile
from langchain.document_loaders import NotebookLoader

from .common import process_file


def process_ipnyb(file: UploadFile, enable_summarization, user):
    return process_file(file, NotebookLoader, "ipynb", enable_summarization, user)
