from langchain.document_loaders import PythonLoader
from models import File

from .common import process_file


async def process_python(file: File, brain_id):
    return await process_file(
        file=file,
        loader_class=PythonLoader,
        brain_id=brain_id,
    )
