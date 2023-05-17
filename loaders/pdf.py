from .common import process_file
from langchain.document_loaders import PyPDFLoader


def process_pdf(vector_store, file, stats_db):
    return process_file(vector_store, file, PyPDFLoader, ".pdf", stats_db=stats_db)
