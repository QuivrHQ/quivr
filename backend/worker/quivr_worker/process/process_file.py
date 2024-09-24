from typing import Any

from langchain_core.documents import Document
from quivr_api.logger import get_logger
from quivr_api.modules.knowledge.entity.knowledge import KnowledgeDB
from quivr_api.modules.vector.service.vector_service import VectorService
from quivr_core.files.file import QuivrFile
from quivr_core.processor.registry import get_processor_class

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


async def store_chunks(
    *,
    knowledge: KnowledgeDB,
    chunks: list[Document],
    vector_service: VectorService,
):
    assert knowledge.id
    vector_ids = await vector_service.create_vectors(chunks, knowledge.id)
    logger.debug(
        f"Inserted {len(chunks)} chunks in vectors table for knowledge: {knowledge.id}"
    )
    if vector_ids is None or len(vector_ids) == 0:
        raise Exception(f"Error inserting chunks for  knowledge {knowledge.id}")


async def parse_qfile(
    *,
    qfile: QuivrFile,
    **processor_kwargs: dict[str, Any],
) -> list[Document]:
    try:
        # TODO(@aminediro): add audio procesors to quivr-core
        if qfile.file_extension in audio_extensions:
            logger.debug(f"processing audio file {qfile}")
            audio_docs = process_audio_file(qfile)
            return audio_docs
        else:
            processor_cls = get_processor_class(qfile.file_extension)
            processor = processor_cls(**processor_kwargs)
            docs = await processor.process_file(qfile)
            logger.debug(f"Parsed {qfile} to : {docs}")
            return docs
    except KeyError as e:
        raise ValueError(f"Can't parse {qfile}. No available processor") from e


# TODO: Move this to quivr-core
def process_audio_file(
    qfile: QuivrFile,
):
    try:
        result = process_audio(file=qfile)
        if result is None or result == 0:
            logger.info(
                f"{qfile.file_name} has been uploaded to brain. There might have been an error while reading it, please make sure the file is not illformed or just an image",  # pyright: ignore reportPrivateUsage=none
            )
            return []
        return result
    except Exception as e:
        logger.exception(f"Error processing audio file {qfile}: {e}")
        raise e
