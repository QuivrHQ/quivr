from langchain.document_loaders import UnstructuredPDFLoader
from models import File

from .common import process_file


# TODO(pg): different mode can be used to UnstructuredPDFLoader like "paged"
# => check the docs!
def process_pdf(file: File, brain_id):
    return process_file(
        file=file,
        loader_class=UnstructuredPDFLoader,
        brain_id=brain_id,
    )
