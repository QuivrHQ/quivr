from fastapi import UploadFile
from langchain.document_loaders import UnstructuredMarkdownLoader
from models.settings import CommonsDep

from .common import process_file


def process_markdown(commons: CommonsDep, file: UploadFile, enable_summarization, user, user_openai_api_key):
    return process_file(commons, file, UnstructuredMarkdownLoader, ".md", enable_summarization, user, user_openai_api_key)
