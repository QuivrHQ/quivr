import hashlib
import os
import time
from contextlib import contextmanager
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Generator, Tuple

from quivr_api.celery_config import celery
from quivr_api.logger import get_logger
from quivr_api.modules.knowledge.dto.outputs import KnowledgeDTO
from quivr_api.modules.knowledge.entity.knowledge import KnowledgeDB, KnowledgeSource
from quivr_api.modules.sync.dto.outputs import SyncProvider
from quivr_api.modules.sync.utils.sync import (
    AzureDriveSync,
    BaseSync,
    DropboxSync,
    GitHubSync,
    GoogleDriveSync,
)
from quivr_core.files.file import FileExtension, QuivrFile

from quivr_worker.parsers.crawler import slugify

celery_inspector = celery.control.inspect()

logger = get_logger("celery_worker")


def skip_process(knowledge: KnowledgeDTO | KnowledgeDB) -> bool:
    return knowledge.is_folder and knowledge.source != KnowledgeSource.NOTION


def build_syncprovider_mapping() -> dict[SyncProvider, BaseSync]:
    mapping_sync_utils = {
        SyncProvider.GOOGLE: GoogleDriveSync(),
        SyncProvider.AZURE: AzureDriveSync(),
        SyncProvider.DROPBOX: DropboxSync(),
        SyncProvider.GITHUB: GitHubSync(),
        # SyncProvider.NOTION: NotionSync(notion_service=notion_service),
    }
    return mapping_sync_utils


def compute_sha1(content: bytes) -> str:
    m = hashlib.sha1()
    m.update(content)
    return m.hexdigest()


def get_tmp_name(file_name: str) -> Tuple[str, str, str]:
    # Filepath is S3 based
    tmp_name = file_name.replace("/", "_")
    base_file_name = os.path.basename(file_name)
    _, file_extension = os.path.splitext(base_file_name)
    return tmp_name, base_file_name, file_extension


@contextmanager
def create_temp_file(
    file_data: bytes,
    file_name_ext: str,
):
    # TODO(@aminediro) :
    # Maybe use fsspec file to be agnostic to where files are stored
    # We are reading the whole file to memory, which doesn't scale
    try:
        tmp_name, _, _ = get_tmp_name(file_name_ext)
        tmp_file = NamedTemporaryFile(
            suffix="_" + tmp_name,
        )
        tmp_file.write(file_data)
        tmp_file.flush()
        yield Path(tmp_file.name)
    finally:
        tmp_file.close()


@contextmanager
def build_qfile(
    knowledge: KnowledgeDB, file_data: bytes
) -> Generator[QuivrFile, None, None]:
    assert knowledge.id
    assert knowledge.file_sha1
    if knowledge.source == KnowledgeSource.WEB:
        file_name = slugify(knowledge.url) + ".txt"
        extension = FileExtension.txt
    else:
        assert knowledge.file_name
        file_name = knowledge.file_name
        extension = FileExtension(knowledge.extension)

    with create_temp_file(
        file_data=file_data, file_name_ext=file_name
    ) as tmp_file_path:
        qfile = QuivrFile(
            id=knowledge.id,
            original_filename=file_name,
            path=tmp_file_path,
            file_sha1=knowledge.file_sha1,
            file_extension=extension,
            file_size=len(file_data),
            metadata={
                "date": time.strftime("%Y%m%d"),
                "file_name": knowledge.file_name,
                "knowledge_id": knowledge.id,
            },
        )
        if knowledge.metadata_:
            qfile.additional_metadata = {
                **qfile.metadata,
                **knowledge.metadata_,
            }
        yield qfile
