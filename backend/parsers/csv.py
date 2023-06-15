from fastapi import UploadFile
from langchain.document_loaders.csv_loader import CSVLoader
from utils.common import CommonsDep

from .common import process_file


def process_csv(commons: CommonsDep, file: UploadFile, enable_summarization, user, user_openai_api_key):
    return process_file(commons, file, CSVLoader, ".csv", enable_summarization, user, user_openai_api_key)
