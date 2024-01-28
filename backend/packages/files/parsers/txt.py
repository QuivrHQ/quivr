from langchain.document_loaders import TextLoader
from models import File

from .common import process_file


async def process_txt(
    file: File,
    brain_id,
    original_file_name,
):
    return await process_file(
        file=file,
        loader_class=TextLoader,
        brain_id=brain_id,
        original_file_name=original_file_name,
    )
