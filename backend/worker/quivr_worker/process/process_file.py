from typing import Any
from uuid import UUID

from langchain_core.documents import Document
from quivr_api.logger import get_logger
from quivr_api.modules.brain.entity.brain_entity import BrainEntity
from quivr_api.modules.brain.service.brain_service import BrainService
from quivr_api.modules.vector.service.vector_service import VectorService
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
    store_chunks(
        file=file_instance,
        brain_id=brain.brain_id,
        chunks=chunks,
        brain_service=brain_service,
        vector_service=vector_service,
    )


def store_chunks(
    *,
    file: File,
    brain_id: UUID,
    chunks: list[Document],
    brain_service: BrainService,
    vector_service: VectorService,
):
    # vector_ids = document_vector_store.add_documents(chunks)
    vector_ids = vector_service.create_vectors(chunks, file.id)
    logger.debug(f"Inserted {len(chunks)} chunks in vectors table for {file}")

    if vector_ids is None or len(vector_ids) == 0:
        raise Exception(f"Error inserting chunks for file {file.file_name}")

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
            processor = processor_cls(**processor_kwargs)
            docs = await processor.process_file(qfile)
            logger.debug(f"Parsed {qfile} to : {docs}")
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
