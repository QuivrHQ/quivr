from quivr_api.logger import get_logger
from quivr_api.modules.brain.entity.brain_entity import BrainEntity

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


def process_file(
    file: File,
    brain: BrainEntity,
    original_file_name=None,
    integration=None,
    integration_link=None,
):
    # FIXME: @chloedia @AmineDiro
    # TODO: These check should happen at API level in Knowledge table
    # file_exists = file_already_exists()
    # file_exists_in_brain = file_already_exists_in_brain(brain.brain_id)

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
    else:
        logger.error(
            f"❌ {file.file_name} is not supported.",  # pyright: ignore reportPrivateUsage=none
            "error",
        )
