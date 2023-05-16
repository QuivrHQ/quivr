from .common import process_file
from langchain.document_loaders import Docx2txtLoader

def process_docx(vector_store, file):
    return process_file(vector_store, file, Docx2txtLoader, ".docx")