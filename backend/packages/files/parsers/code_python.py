from langchain.document_loaders import PythonLoader
from models import File

from .common import process_file


async def process_python(file: File, brain_id, original_file_name):
    return await process_file(
        file=file,
        loader_class=PythonLoader,
        brain_id=brain_id,
        original_file_name=original_file_name,
    )
