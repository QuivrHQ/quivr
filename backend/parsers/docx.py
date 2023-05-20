from .common import process_file
from langchain.document_loaders import Docx2txtLoader
from fastapi import UploadFile

def process_docx(vector_store, file: UploadFile, stats_db):
    return process_file(vector_store, file, Docx2txtLoader, ".docx", stats_db=stats_db)