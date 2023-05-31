from fastapi import UploadFile
from langchain.document_loaders.csv_loader import CSVLoader

from .common import process_file


def process_csv(file: UploadFile, enable_summarization, user):
    return process_file(file, CSVLoader, ".csv", enable_summarization, user)
