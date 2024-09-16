import mimetypes
from io import BufferedReader, FileIO

from quivr_api.logger import get_logger
from quivr_api.modules.dependencies import get_supabase_async_client
from quivr_api.modules.knowledge.entity.knowledge import KnowledgeDB
from quivr_api.modules.knowledge.repository.storage_interface import StorageInterface

logger = get_logger(__name__)


class SupabaseS3Storage(StorageInterface):
    def __init__(self):
        self.client = None

    async def _set_client(self):
        if self.client is None:
            self.client = await get_supabase_async_client()

    def get_storage_path(
        self,
        knowledge: KnowledgeDB,
    ) -> str:
        if knowledge.id is None:
            raise ValueError("knowledge should have a valid id")
        return str(knowledge.id)

    async def upload_file_storage(
        self,
        knowledge: KnowledgeDB,
        knowledge_data: FileIO | BufferedReader | bytes,
        upsert: bool = False,
    ):
        await self._set_client()
        assert self.client

        mime_type = "application/html"
        if knowledge.file_name:
            guessed_mime_type, _ = mimetypes.guess_type(knowledge.file_name)
            mime_type = guessed_mime_type or mime_type

        storage_path = self.get_storage_path(knowledge)
        logger.info(
            f"Uploading file to s3://quivr/{storage_path} using supabase. upsert={upsert}, mimetype={mime_type}"
        )

        if upsert:
            _ = await self.client.storage.from_("quivr").update(
                storage_path,
                knowledge_data,
                file_options={
                    "content-type": mime_type,
                    "upsert": "true",
                    "cache-control": "3600",
                },
            )
            return storage_path
        else:
            # check if file sha1 is already in storage
            try:
                _ = await self.client.storage.from_("quivr").upload(
                    storage_path,
                    knowledge_data,
                    file_options={
                        "content-type": mime_type,
                        "upsert": "false",
                        "cache-control": "3600",
                    },
                )
                return storage_path

            except Exception as e:
                if "The resource already exists" in str(e) and not upsert:
                    raise FileExistsError(f"File {storage_path} already exists")
                raise e

    async def remove_file(self, storage_path: str):
        """
        Remove file from storage
        """
        await self._set_client()
        assert self.client
        try:
            response = await self.client.storage.from_("quivr").remove([storage_path])
            return response
        except Exception as e:
            logger.error(e)
