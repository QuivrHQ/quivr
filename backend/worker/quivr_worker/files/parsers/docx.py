from langchain_community.document_loaders import Docx2txtLoader
from quivr_api.models.files import File

from .common import process_file


def process_docx(
    file: File, brain_id, original_file_name, integration=None, integration_link=None
):
    return process_file(
        file=file,
        loader_class=Docx2txtLoader,
        brain_id=brain_id,
        original_file_name=original_file_name,
        integration=integration,
        integration_link=integration_link,
    )
