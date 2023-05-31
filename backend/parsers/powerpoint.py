from fastapi import UploadFile
from langchain.document_loaders import UnstructuredPowerPointLoader

from .common import process_file


def process_powerpoint(file: UploadFile, enable_summarization, user):
    return process_file(file, UnstructuredPowerPointLoader, ".pptx", enable_summarization, user)
