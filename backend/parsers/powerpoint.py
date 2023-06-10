from fastapi import UploadFile
from langchain.document_loaders import UnstructuredPowerPointLoader

from .common import process_file


def process_powerpoint(file: UploadFile, enable_summarization, user, user_openai_api_key):
    return process_file(file, UnstructuredPowerPointLoader, ".pptx", enable_summarization, user, user_openai_api_key)
