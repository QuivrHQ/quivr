from fastapi import UploadFile
from langchain.document_loaders import UnstructuredODTLoader
from models.settings import CommonsDep

from .common import process_file


def process_odt(commons: CommonsDep, file: UploadFile, enable_summarization, brain_id, user_openai_api_key):
    return process_file(commons, file, UnstructuredODTLoader, ".odt", enable_summarization, brain_id, user_openai_api_key)
