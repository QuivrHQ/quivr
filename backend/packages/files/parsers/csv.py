from langchain.document_loaders import CSVLoader
from models import File

from .common import process_file


def process_csv(
    file: File,
    brain_id,
):
    return process_file(
        file=file,
        loader_class=CSVLoader,
        brain_id=brain_id,
    )
