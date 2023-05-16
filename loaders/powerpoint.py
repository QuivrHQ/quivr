from .common import process_file
from langchain.document_loaders import UnstructuredPowerPointLoader

def process_powerpoint(vector_store, file):
    return process_file(vector_store, file, UnstructuredPowerPointLoader, ".pptx")