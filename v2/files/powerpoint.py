from .common import process_file
from langchain.document_loaders import UnstructuredPowerPointLoader
from fastapi import UploadFile

def process_powerpoint(vector_store, file: UploadFile, stats_db):
    return process_file(vector_store, file, UnstructuredPowerPointLoader, ".pptx", stats_db=stats_db)