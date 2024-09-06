import mimetypes
from io import BufferedReader, FileIO

from quivr_api.logger import get_logger
from quivr_api.modules.dependencies import get_supabase_async_client
from quivr_api.modules.knowledge.repository.storage_interface import StorageInterface

logger = get_logger(__name__)


class SupabaseS3Storage(StorageInterface):
    def __init__(self):
        self.client = None

    async def _set_client(self):
        if self.client is None:
            self.client = await get_supabase_async_client()

    async def upload_file_storage(
        self,
        file: FileIO | BufferedReader | bytes,
        storage_path: str,
        upsert: bool = False,
    ):
        await self._set_client()
        assert self.client
        mime_type, _ = mimetypes.guess_type(storage_path)
        logger.debug(
            f"Uploading file to {storage_path} using supabase. upsert={upsert}, mimetype={mime_type}"
        )

        if upsert:
            response = await self.client.storage.from_("quivr").update(
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
            # check if file sha1 is already in storage
            try:
                response = await self.client.storage.from_("quivr").upload(
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
                if "The resource already exists" in str(e) and not upsert:
                    raise FileExistsError(f"File {storage_path} already exists")
                raise e

    async def remove_file(self, file_name: str):
        """
        Remove file from storage
        """
        await self._set_client()
        assert self.client
        try:
            response = await self.client.storage.from_("quivr").remove([file_name])
            return response
        except Exception as e:
            logger.error(e)
