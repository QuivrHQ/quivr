from langchain.document_loaders import UnstructuredPDFLoader
from models import File

from .common import process_file


def process_odt(file: File, brain_id):
    return process_file(
        file=file,
        loader_class=UnstructuredPDFLoader,
        brain_id=brain_id,
    )
