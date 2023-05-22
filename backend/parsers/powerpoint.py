from .common import process_file
from langchain.document_loaders import UnstructuredPowerPointLoader
from fastapi import UploadFile


def process_powerpoint(file: UploadFile, enable_summarization):
    return process_file(file, UnstructuredPowerPointLoader, ".pptx", enable_summarization)
