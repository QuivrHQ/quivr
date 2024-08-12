import mimetypes
from io import BufferedReader, FileIO

from supabase.client import Client

from quivr_api.logger import get_logger
from quivr_api.models.settings import get_supabase_async_client, get_supabase_client

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
        logger.debug(f"File identifier: {file_identifier} exists: {file_exists}")
        if file_exists:
            return True
        else:
            return False
    except Exception as e:
        logger.error(f"An error occurred while checking the file: {e}")
        return True


async def upload_file_storage(
    file: FileIO | BufferedReader | bytes,
    storage_path: str,
    upsert: bool = False,
):
    supabase_client = await get_supabase_async_client()
    mime_type, _ = mimetypes.guess_type(storage_path)
    logger.debug(
        f"Uploading file to {storage_path} using supabase. upsert={upsert}, mimetype={mime_type}"
    )

    if upsert:
        response = await supabase_client.storage.from_("quivr").update(
            storage_path,
            file,  # type: ignore
            file_options={
                "content-type": mime_type or "application/html",
                "upsert": "true",
                "cache-control": "3600",
            },
        )
        return response
    else:
        try:
            response = await supabase_client.storage.from_("quivr").upload(
                storage_path,
                file,  # type: ignore
                file_options={
                    "content-type": mime_type or "application/html",
                    "upsert": "false",
                    "cache-control": "3600",
                },
            )
            return response
        except Exception as e:
            # FIXME: Supabase client to return the correct error
            if "The resource already exists" in str(e) and not upsert:
                raise FileExistsError(f"File {storage_path} already exists")
            raise e
