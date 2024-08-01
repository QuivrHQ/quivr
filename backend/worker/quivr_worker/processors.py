from uuid import UUID

from quivr_api.modules.brain.service.brain_service import BrainService

from .parsers.audio import process_audio

file_processors = {
    ".m4a": process_audio,
    ".mp3": process_audio,
    ".webm": process_audio,
    ".mp4": process_audio,
    ".mpga": process_audio,
    ".wav": process_audio,
    ".mpeg": process_audio,
}


def create_response(message, type):
    return {"message": message, "type": type}


brain_service = BrainService()


# TODO: Move filter_file to a file service to avoid circular imports from quivr_api.models/files.py for File class
def process_file(
    file,
    brain_id: UUID,
    original_file_name=None,
    integration=None,
    integration_link=None,
):
    file_exists = file.file_already_exists()
    file_exists_in_brain = file.file_already_exists_in_brain(brain_id)
    using_file_name = file.file_name

    brain = brain_service.get_brain_by_id(brain_id)
    if brain is None:
        raise Exception("It seems like you're uploading knowledge to an unknown brain.")

    if file_exists_in_brain:
        return create_response(
            f"🤔 {using_file_name} already exists in brain {brain.name}.",  # pyright: ignore reportPrivateUsage=none
            "warning",
        )
    elif file.file_is_empty():
        return create_response(
            f"❌ {original_file_name} is empty.",  # pyright: ignore reportPrivateUsage=none
            "error",  # pyright: ignore reportPrivateUsage=none
        )
    elif file_exists:
        file.link_file_to_brain(brain_id)
        return create_response(
            f"✅ {using_file_name} has been uploaded to brain {brain.name}.",  # pyright: ignore reportPrivateUsage=none
            "success",
        )

    if file.file_extension in file_processors:
        try:
            result = file_processors[file.file_extension](
                file=file,
                brain_id=brain_id,
                original_file_name=original_file_name,
                integration=integration,
                integration_link=integration_link,
            )
            if result is None or result == 0:
                return create_response(
                    f"？ {using_file_name} has been uploaded to brain. There might have been an error while reading it, please make sure the file is not illformed or just an image",  # pyright: ignore reportPrivateUsage=none
                    "warning",
                )
            return create_response(
                f"✅ {using_file_name} has been uploaded to brain {brain.name} in {result} chunks",  # pyright: ignore reportPrivateUsage=none
                "success",
            )
        except Exception as e:
            # Add more specific exceptions as needed.
            print(f"Error processing file: {e}")
            raise e

    return create_response(
        f"❌ {using_file_name} is not supported.",  # pyright: ignore reportPrivateUsage=none
        "error",
    )
