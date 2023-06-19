from fastapi import UploadFile
from langchain.document_loaders.epub import UnstructuredEPubLoader
from utils.common import CommonsDep

from .common import process_file


def process_epub(commons: CommonsDep, file: UploadFile, enable_summarization, user, user_openai_api_key):
    return process_file(commons, file, UnstructuredEPubLoader, ".epub", enable_summarization, user, user_openai_api_key)
