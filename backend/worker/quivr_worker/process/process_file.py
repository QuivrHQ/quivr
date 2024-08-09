from typing import Any
from uuid import UUID

from langchain_core.documents import Document
from quivr_api.logger import get_logger
from quivr_api.modules.brain.entity.brain_entity import BrainEntity
from quivr_api.modules.brain.service.brain_service import BrainService
from quivr_api.modules.brain.service.brain_vector_service import BrainVectorService
from quivr_api.vector.service.vector_service import VectorService
from quivr_core.processor.registry import get_processor_class

from quivr_worker.files import File
from quivr_worker.parsers.audio import process_audio

logger = get_logger("celery_worker")

# TODO: remove global
audio_extensions = {
    ".m4a",
    ".mp3",
    ".webm",
    ".mp4",
    ".mpga",
    ".wav",
    ".mpeg",
}


async def process_file(
    file_instance: File,
    brain: BrainEntity,
    brain_service: BrainService,
    brain_vector_service: BrainVectorService,
    vector_service: VectorService,
    integration: str | None,
    integration_link: str | None,
):
    chunks = await parse_file(
        file=file_instance,
        brain=brain,
        integration=integration,
        integration_link=integration_link,
    )
    await store_chunks(
        file=file_instance,
        brain_id=brain.brain_id,
        chunks=chunks,
        brain_service=brain_service,
        brain_vector_service=brain_vector_service,
        vector_service=vector_service,
    )


async def store_chunks(
    *,
    file: File,
    brain_id: UUID,
    chunks: list[Document],
    brain_service: BrainService,
    brain_vector_service: BrainVectorService,
    vector_service: VectorService,
):
    # vector_ids = document_vector_store.add_documents(chunks)
    vector_ids = await vector_service.create_vectors(chunks, file.id)
    logger.debug(f"Inserted {len(chunks)} chunks in vectors table for {file}")

    if vector_ids is None or len(vector_ids) == 0:
        raise Exception(f"Error inserting chunks for file {file.file_name}")

    # TODO(@chloedia) : Brains should be associated with knowledge NOT vectors...
    # for created_vector_id in vector_ids:
    #     result = brain_vector_service.create_brain_vector(
    #         created_vector_id, file.file_sha1
    #     )
    #     logger.debug(f"Inserted : {len(result)} in brain_vectors for {file}")

    # assert isinstance(document_vector_store, CustomSupabaseVectorStore), f'Expected document_vector_store to be a CustomSupabaseVectorStore, got {document_vector_store}'
    # for created_vector_id in vector_ids:
    #     logger.debug(f"Adding knowledge_id {file.id} to vector_id {created_vector_id}")
    #     document_vector_store.add_knowledge_id_to_vector(vector_id = UUID(created_vector_id), knowledge_id = file.id)
    brain_service.update_brain_last_update_time(brain_id)


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
            logger.debug(f"processing audio file {file}")
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
            docs = await processor.process_file(qfile)
            logger.debug(f"parsed {file} to : {docs}")
            return docs
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
