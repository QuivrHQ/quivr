import os
from io import BufferedReader, FileIO

from supabase.client import Client

from quivr_api.logger import get_logger
from quivr_api.models.settings import get_supabase_async_client, get_supabase_client

logger = get_logger(__name__)


# Mapping of file extensions to MIME types
mime_types = {
    ".txt": "text/plain",
    ".csv": "text/csv",
    ".md": "text/markdown",
    ".markdown": "text/markdown",
    ".telegram": "application/x-telegram",
    ".m4a": "audio/mp4",
    ".mp3": "audio/mpeg",
    ".webm": "audio/webm",
    ".mp4": "video/mp4",
    ".mpga": "audio/mpeg",
    ".wav": "audio/wav",
    ".mpeg": "video/mpeg",
    ".pdf": "application/pdf",
    ".html": "text/html",
    ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ".odt": "application/vnd.oasis.opendocument.text",
    ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ".xls": "application/vnd.ms-excel",
    ".epub": "application/epub+zip",
    ".ipynb": "application/x-ipynb+json",
    ".py": "text/x-python",
}


def check_file_exists(brain_id: str, file_identifier: str) -> bool:
    supabase_client: Client = get_supabase_client()
    try:
        # Check if the file exists
        logger.info(f"Checking if file {file_identifier} exists.")
        # This needs to be converted into a file_identifier that is safe for a URL

        response = supabase_client.storage.from_("quivr").list(brain_id)

        # Check if the file_identifier is in the response
        file_exists = any(
            file["name"].split(".")[0] == file_identifier.split(".")[0]
            for file in response
        )
        logger.info(f"File identifier: {file_identifier}")
        logger.info(f"File exists: {file_exists}")
        if file_exists:
            logger.info(f"File {file_identifier} exists.")
            return True
        else:
            logger.info(f"File {file_identifier} does not exist.")
            return False
    except Exception as e:
        logger.error(f"An error occurred while checking the file: {e}")
        return True


async def upload_file_storage(
    file: FileIO | BufferedReader | bytes,
    file_identifier: str,
    upsert: bool = False,
):
    supabase_client = await get_supabase_async_client()
    response = None

    _, file_extension = os.path.splitext(file_identifier)
    mime_type = mime_types.get(file_extension, "text/html")

    if upsert:
        response = supabase_client.storage.from_("quivr").update(
            file_identifier,
            file,  # type: ignore
            file_options={
                "content-type": mime_type,
                "upsert": "true",
                "cache-control": "3600",
            },
        )
    else:
        try:
            response = await supabase_client.storage.from_("quivr").upload(
                file_identifier,
                file,  # type: ignore
                file_options={
                    "content-type": mime_type,
                    "upsert": "false",
                    "cache-control": "3600",
                },
            )
        except Exception as e:
            # TODO: Supabase client should return the correct erro
            if "The resource already exists" in str(e) and not upsert:
                raise FileExistsError("The resource already exists")
            raise e

    return response
