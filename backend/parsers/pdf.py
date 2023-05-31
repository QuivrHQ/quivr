from fastapi import UploadFile
from langchain.document_loaders import PyPDFLoader

from .common import process_file


def process_pdf(file: UploadFile, enable_summarization, user):
    return process_file(file, PyPDFLoader, ".pdf", enable_summarization, user)
