from .common import process_file
from langchain.document_loaders import PyPDFLoader


def process_pdf(vector_store, file):
    return process_file(vector_store, file, PyPDFLoader, ".pdf")
