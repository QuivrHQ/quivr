from fastapi import UploadFile
from langchain.document_loaders import UnstructuredPowerPointLoader
from utils.common import CommonsDep

from .common import process_file


def process_powerpoint(commons: CommonsDep, file: UploadFile, enable_summarization, user, user_openai_api_key):
    return process_file(commons, file, UnstructuredPowerPointLoader, ".pptx", enable_summarization, user, user_openai_api_key)
