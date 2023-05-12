from .common import process_file
from langchain.document_loaders import UnstructuredMarkdownLoader

def process_markdown(vector_store, file):
    return process_file(vector_store, file, UnstructuredMarkdownLoader, ".md")
