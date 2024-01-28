from langchain.document_loaders import CSVLoader
from models import File

from .common import process_file


def process_csv(file: File, brain_id, original_file_name):
    return process_file(
        file=file,
        loader_class=CSVLoader,
        brain_id=brain_id,
        original_file_name=original_file_name,
    )
