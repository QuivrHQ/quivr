from .common import process_file
from langchain.document_loaders.csv_loader import CSVLoader

def process_csv(vector_store, file,stats_db):
    return process_file(vector_store, file, CSVLoader, ".csv",stats_db=stats_db)