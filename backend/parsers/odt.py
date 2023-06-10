from fastapi import UploadFile
from langchain.document_loaders import UnstructuredODTLoader

from .common import process_file


def process_odt(file: UploadFile, enable_summarization, user, user_openai_api_key):
    return process_file(file, UnstructuredODTLoader, ".odt", enable_summarization, user, user_openai_api_key)
