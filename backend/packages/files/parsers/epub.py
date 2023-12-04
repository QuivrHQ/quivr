from langchain.document_loaders.epub import UnstructuredEPubLoader
from models import File

from .common import process_file


def process_epub(file: File, brain_id):
    return process_file(
        file=file,
        loader_class=UnstructuredEPubLoader,
        brain_id=brain_id,
    )
