from .common import process_file
from langchain.document_loaders import PyPDFLoader
from fastapi import UploadFile


def process_pdf(file: UploadFile, enable_summarization):
    return process_file(file, PyPDFLoader, ".pdf", enable_summarization)
