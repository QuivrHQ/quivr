import mimetypes
import os
from io import BufferedReader, FileIO

from supabase.client import AsyncClient, Client

from quivr_api.logger import get_logger
from quivr_api.models.settings import get_supabase_client

logger = get_logger(__name__)


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
    supabase_client: AsyncClient,
    file: FileIO | BufferedReader | bytes,
    file_name: str,
    upsert: bool = False,
):
    _, file_extension = os.path.splitext(file_name)
    mime_type, _ = mimetypes.guess_type(file_name)
    logger.debug(f"Uploading {file_name} to supabase storage.")

    if upsert:
        response = supabase_client.storage.from_("quivr").update(
            file_name,
            file,  # type: ignore
            file_options={
                "content-type": mime_type or "txt/html",
                "upsert": "true",
                "cache-control": "3600",
            },
        )
    else:
        try:
            response = await supabase_client.storage.from_("quivr").upload(
                file_name,
                file,  # type: ignore
                file_options={
                    "content-type": mime_type or "text/html",
                    "upsert": "false",
                    "cache-control": "3600",
                },
            )
            return response
        except Exception as e:
            # FIXME: Supabase client to return the correct error
            if "The resource already exists" in str(e) and not upsert:
                raise FileExistsError("The resource already exists")
            raise e
