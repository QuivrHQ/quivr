from .common import process_file
from langchain.document_loaders import UnstructuredHTMLLoader

def process_html(vector_store, file):
    return process_file(vector_store, file, UnstructuredHTMLLoader, ".html")