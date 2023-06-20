from fastapi import UploadFile
from langchain.document_loaders import Docx2txtLoader
from models.settings import CommonsDep

from .common import process_file


def process_docx(commons: CommonsDep, file: UploadFile, enable_summarization, user, user_openai_api_key):
    return process_file(commons, file, Docx2txtLoader, ".docx", enable_summarization, user, user_openai_api_key)
