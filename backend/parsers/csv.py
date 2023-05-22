from .common import process_file
from langchain.document_loaders.csv_loader import CSVLoader
from fastapi import UploadFile


def process_csv(file: UploadFile, enable_summarization):
    return process_file(file, CSVLoader, ".csv", enable_summarization)
