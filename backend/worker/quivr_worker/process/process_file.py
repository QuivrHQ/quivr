import time
from contextlib import contextmanager
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any
from uuid import UUID, uuid4

from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStore
from quivr_api.logger import get_logger
from quivr_api.modules.brain.entity.brain_entity import BrainEntity
from quivr_api.modules.brain.service.brain_service import BrainService
from quivr_api.modules.brain.service.brain_vector_service import BrainVectorService
from quivr_core.files.file import FileExtension, QuivrFile
from quivr_core.processor.registry import get_processor_class
from supabase import Client

from quivr_worker.files import File
from quivr_worker.utils import get_tmp_name

from ..parsers.audio import process_audio

logger = get_logger("celery_worker")

file_processors = {
    ".m4a": process_audio,
    ".mp3": process_audio,
    ".webm": process_audio,
    ".mp4": process_audio,
    ".mpga": process_audio,
    ".wav": process_audio,
    ".mpeg": process_audio,
}


@contextmanager
def build_local_file(
    supabase_client: Client, file_name: str, bucket_name: str = "quivr"
):
    try:
        # FIXME: @chloedia @AmineDiro
        # We should decide if these checks should happen at API level or Worker level
        # These checks should use Knowledge table (where we should store knowledge sha1)
        # file_exists = file_already_exists()
        # file_exists_in_brain = file_already_exists_in_brain(brain.brain_id)
        # TODO(@aminediro) : Maybe use fsspec file to be agnostic to where files are stored :?
        # We are reading the whole file to memory, which doesn't scale
        tmp_name, base_file_name, file_extension = get_tmp_name(file_name)
        tmp_file = NamedTemporaryFile(
            suffix="_" + tmp_name,  # pyright: ignore reportPrivateUsage=none
        )

        file_data = supabase_client.storage.from_(bucket_name).download(file_name)
        tmp_file.write(file_data)
        tmp_file.flush()
        file_instance = File(
            file_name=base_file_name,
            tmp_file_path=Path(tmp_file.name),
            bytes_content=file_data,
            file_size=len(file_data),
            file_extension=file_extension,
        )
        yield file_instance
    finally:
        # Code to release resource, e.g.:
        tmp_file.close()


async def process_file_func(
    brain_service: BrainService,
    brain_vector_service: BrainVectorService,
    supabase_client: Client,
    document_vector_store: VectorStore,
    file_name: str,
    brain_id: UUID,
    file_original_name: str,
    knowledge_id: UUID,
    integration: str | None = None,
    integration_link: str | None = None,
    delete_file: bool = False,
):
    brain = brain_service.get_brain_by_id(brain_id)
    if brain is None:
        logger.exception(
            "It seems like you're uploading knowledge to an unknown brain."
        )
        return True

    with build_local_file(supabase_client, file_name) as file_instance:
        # TODO(@StanGirard): fix bug
        # NOTE (@aminediro): I think this might be related to knowledge delete timeouts ?
        if delete_file:
            brain_vector_service.delete_file_from_brain(
                file_original_name, only_vectors=True
            )
        chunks = await parse_file(
            file=file_instance,
            knowledge_id=knowledge_id,
            brain=brain,
            integration=integration,
            integration_link=integration_link,
        )
        store_chunks(
            file=file_instance,
            brain_id=brain_id,
            chunks=chunks,
            document_vector_store=document_vector_store,
            brain_service=brain_service,
            brain_vector_service=brain_vector_service,
        )


def store_chunks(
    *,
    file: File,
    brain_id: UUID,
    chunks: list[Document],
    brain_service: BrainService,
    brain_vector_service: BrainVectorService,
    document_vector_store: VectorStore,
):
    vector_ids = document_vector_store.add_documents(chunks)
    logger.debug(f"Inserted {len(chunks)} chunks in vectors table for {file}")
    assert (
        vector_ids and len(vector_ids) > 0
    ), f"Error inserting chunks for file {file.file_name}"

    # TODO(@chloedia) : Brains should be associated with knowledge NOT vectors...
    for created_vector_id in vector_ids:
        result = brain_vector_service.create_brain_vector(
            created_vector_id, file.file_sha1
        )
        logger.debug(f"Inserted : {len(result)} in brain_vectors for {file}")
    brain_service.update_brain_last_update_time(brain_id)
    pass


async def parse_file(
    file: File,
    brain: BrainEntity,
    knowledge_id: UUID | None = None,
    integration: str | None = None,
    integration_link: str | None = None,
    **processor_kwargs: dict[str, Any],
) -> list[Document]:
    qfile = QuivrFile(
        id=uuid4(),  # TODO(@chloedia @aminediro) : should be the id for knowledge
        original_filename=file.file_name,
        path=file.tmp_file_path,
        brain_id=brain.brain_id,
        file_sha1=file.file_sha1,
        file_extension=FileExtension[file.file_extension],
        file_size=file.file_size,
        metadata={
            "date": time.strftime("%Y%m%d"),
            "original_file_name": file.file_name,
            "knowledge_id": knowledge_id,  # TODO(@chloedia): This knowledge_id should be a column in vectors table
            "integration": integration or "",
            "integration_link": integration_link or "",
        },
    )
    try:
        # TODO(@aminediro):
        # Check first if audio -> Send to different function
        if file.file_extension:
            processor_cls = get_processor_class(file.file_extension)
            logger.debug(f"processing {file} using class {processor_cls.__name__}")
            processor = processor_cls(**processor_kwargs)
            docs = await processor.process_file(qfile)
            return docs
        else:
            logger.error(f"can't find processor for {file}")
            raise ValueError(f"can't parse {file}. can't find file extension")
    except KeyError as e:
        raise ValueError(f"Can't parse {file}. No available processor") from e


def process_audio_file(
    file: File,
    brain: BrainEntity,
    original_file_name=None,
    integration=None,
    integration_link=None,
):
    if file.file_extension in file_processors:
        try:
            result = file_processors[file.file_extension](
                file=file,
                brain_id=brain.brain_id,
                original_file_name=original_file_name,
                integration=integration,
                integration_link=integration_link,
            )
            if result is None or result == 0:
                return logger.info(
                    f"{file.file_name} has been uploaded to brain. There might have been an error while reading it, please make sure the file is not illformed or just an image",  # pyright: ignore reportPrivateUsage=none
                    "warning",
                )
            return logger.info(
                f"{file.file_name} has been uploaded to brain {brain.name} in {result} chunks",  # pyright: ignore reportPrivateUsage=none
                "success",
            )
        except Exception as e:
            # Add more specific exceptions as needed.
            print(f"Error processing file: {e}")
            raise e
