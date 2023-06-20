from fastapi import UploadFile
from langchain.document_loaders import PyMuPDFLoader
from models.settings import CommonsDep

from .common import process_file


def process_pdf(commons: CommonsDep, file: UploadFile, enable_summarization, user, user_openai_api_key):
    return process_file(commons, file, PyMuPDFLoader, ".pdf", enable_summarization, user, user_openai_api_key)

