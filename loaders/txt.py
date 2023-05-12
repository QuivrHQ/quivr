from .common import process_file
from langchain.document_loaders import TextLoader

def process_txt(vector_store, file):
    return process_file(vector_store, file, TextLoader, ".txt")