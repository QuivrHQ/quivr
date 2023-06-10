from fastapi import UploadFile
from langchain.document_loaders import UnstructuredMarkdownLoader

from .common import process_file


def process_markdown(file: UploadFile, enable_summarization, user, user_openai_api_key):
    return process_file(file, UnstructuredMarkdownLoader, ".md", enable_summarization, user, user_openai_api_key)
