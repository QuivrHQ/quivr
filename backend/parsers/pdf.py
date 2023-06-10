from fastapi import UploadFile
from langchain.document_loaders import PyMuPDFLoader

from .common import process_file


def process_pdf(file: UploadFile, enable_summarization, user, user_openai_api_key):
    return process_file(file, PyMuPDFLoader, ".pdf", enable_summarization, user, user_openai_api_key)
