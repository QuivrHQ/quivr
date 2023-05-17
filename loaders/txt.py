from .common import process_file
from langchain.document_loaders import TextLoader

def process_txt(vector_store, file,stats_db):
    return process_file(vector_store, file, TextLoader, ".txt", stats_db=stats_db)