from fastapi import UploadFile
from langchain.document_loaders import NotebookLoader
from models.settings import CommonsDep

from .common import process_file


def process_ipnyb(commons: CommonsDep, file: UploadFile, enable_summarization, brain_id, user_openai_api_key):
    return process_file(commons, file, NotebookLoader, "ipynb", enable_summarization, brain_id, user_openai_api_key)
