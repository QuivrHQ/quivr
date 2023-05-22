from .common import process_file
from langchain.document_loaders import UnstructuredMarkdownLoader
from fastapi import UploadFile


def process_markdown(file: UploadFile, enable_summarization):
    return process_file(file, UnstructuredMarkdownLoader, ".md", enable_summarization)
