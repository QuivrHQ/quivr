from typing import Any
from uuid import uuid4

from langchain_core.documents import Document
from quivr_api.logger import get_logger
from quivr_api.modules.brain.entity.brain_entity import BrainEntity
from quivr_core.files.file import FileExtension, QuivrFile
from quivr_core.processor.registry import get_processor_class

from quivr_worker.files import File

from .parsers.audio import process_audio

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


async def process_file(
    file: File,
    brain: BrainEntity,
    integration: str | None = None,
    integration_link: str | None = None,
    **processor_kwargs: dict[str, Any],
) -> list[Document]:
    knowledge = []

    qfile = QuivrFile(
        id=uuid4(),  # TODO(@chloedia @aminediro) : should be the id for knowledge
        original_filename=file.file_name,
        path=file.tmp_file_path,
        brain_id=brain.brain_id,
        file_sha1=file.file_sha1,
        file_extension=FileExtension[file.file_extension],
        file_size=file.file_size,
    )

    # TODO:
    # Check first if audio -> Send to different function
    try:
        if file.file_extension:
            processor_cls = get_processor_class(file.file_extension)
            logger.debug(f"processing {file} using class {processor_cls.__name__}")
            processor = processor_cls(**processor_kwargs)
            docs = await processor.process_file(qfile)
            knowledge.extend(docs)
        else:
            logger.error(f"can't find processor for {file}")
            raise ValueError(f"can't parse {file}. can't find file extension")
    except KeyError as e:
        raise Exception(f"Can't parse {file}. No available processor") from e
    return knowledge


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
