from langchain.document_loaders import UnstructuredExcelLoader
from models.files import File

from .common import process_file


def process_xlsx(
    file: File,
    brain_id,
):
    return process_file(
        file=file,
        loader_class=UnstructuredExcelLoader,
        brain_id=brain_id,
    )
