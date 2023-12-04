from langchain.document_loaders import UnstructuredPowerPointLoader
from models import File

from .common import process_file


def process_powerpoint(file: File, brain_id):
    return process_file(
        file=file,
        loader_class=UnstructuredPowerPointLoader,
        brain_id=brain_id,
    )
