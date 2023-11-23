from langchain.document_loaders import UnstructuredMarkdownLoader
from models import File

from .common import process_file


def process_markdown(file: File, brain_id):
    return process_file(
        file=file,
        loader_class=UnstructuredMarkdownLoader,
        brain_id=brain_id,
    )
