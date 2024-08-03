from contextlib import contextmanager
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any
from uuid import UUID

from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStore
from quivr_api.logger import get_logger
from quivr_api.modules.brain.entity.brain_entity import BrainEntity
from quivr_api.modules.brain.service.brain_service import BrainService
from quivr_api.modules.brain.service.brain_vector_service import BrainVectorService
from quivr_core.processor.registry import get_processor_class
from supabase import Client

from quivr_worker.files import File, compute_sha1
from quivr_worker.parsers.audio import process_audio
from quivr_worker.utils import get_tmp_name

logger = get_logger("celery_worker")

audio_extensions = {
    ".m4a",
    ".mp3",
    ".webm",
    ".mp4",
    ".mpga",
    ".wav",
    ".mpeg",
}


@contextmanager
def build_local_file(
    supabase_client: Client,
    knowledge_id: UUID,
    file_name: str,
    bucket_name: str = "quivr",
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
        file_sha1 = compute_sha1(file_data)
        tmp_file.write(file_data)
        tmp_file.flush()

        file_instance = File(
            knowledge_id=knowledge_id,
            file_name=base_file_name,
            tmp_file_path=Path(tmp_file.name),
            file_size=len(file_data),
            file_extension=file_extension,
            file_sha1=file_sha1,
        )
        yield file_instance
    finally:
        # Code to release resource, e.g.:
        tmp_file.close()


async def process_file_func(
    supabase_client: Client,
    brain_service: BrainService,
    brain_vector_service: BrainVectorService,
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

    with build_local_file(supabase_client, knowledge_id, file_name) as file_instance:
        # TODO(@StanGirard): fix bug
        # NOTE (@aminediro): I think this might be related to knowledge delete timeouts ?
        if delete_file:
            brain_vector_service.delete_file_from_brain(
                file_original_name, only_vectors=True
            )
        chunks = await parse_file(
            file=file_instance,
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
    integration: str | None = None,
    integration_link: str | None = None,
    **processor_kwargs: dict[str, Any],
) -> list[Document]:

    try:
        # TODO(@aminediro): add audio procesors to quivr-core
        if file.file_extension in audio_extensions:
            audio_docs = process_audio_file(file, brain)
            return audio_docs
        else:
            qfile = file.to_qfile(
                brain.brain_id,
                {
                    "integration": integration or "",
                    "integration_link": integration_link or "",
                },
            )
            processor_cls = get_processor_class(file.file_extension)
            logger.debug(f"processing {file} using class {processor_cls.__name__}")
            processor = processor_cls(**processor_kwargs)
            audio_docs = await processor.process_file(qfile)
            return audio_docs
    except KeyError as e:
        raise ValueError(f"Can't parse {file}. No available processor") from e


def process_audio_file(
    file: File,
    brain: BrainEntity,
):
    try:
        result = process_audio(file=file)
        if result is None or result == 0:
            logger.info(
                f"{file.file_name} has been uploaded to brain. There might have been an error while reading it, please make sure the file is not illformed or just an image",  # pyright: ignore reportPrivateUsage=none
            )
            return []
        logger.info(
            f"{file.file_name} has been uploaded to brain {brain.name} in {result} chunks",  # pyright: ignore reportPrivateUsage=none
        )
        return result
    except Exception as e:
        logger.exception(f"Error processing audio file {file}: {e}")
        raise e
