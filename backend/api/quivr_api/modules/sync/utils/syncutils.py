import io
import os
from datetime import datetime, timezone
from typing import Any, List, Tuple
from uuid import UUID, uuid4

from supabase.client import AsyncClient

from quivr_api.celery_config import celery
from quivr_api.logger import get_logger
from quivr_api.models.settings import get_supabase_async_client
from quivr_api.modules.brain.repository.brains_vectors import BrainsVectors
from quivr_api.modules.knowledge.dto.inputs import CreateKnowledgeProperties
from quivr_api.modules.knowledge.repository.storage import Storage
from quivr_api.modules.knowledge.service.knowledge_service import KnowledgeService
from quivr_api.modules.notification.dto.inputs import (
    CreateNotification,
    NotificationUpdatableProperties,
)
from quivr_api.modules.notification.entity.notification import NotificationsStatusEnum
from quivr_api.modules.notification.service.notification_service import (
    NotificationService,
)
from quivr_api.modules.sync.dto.inputs import SyncsActiveUpdateInput
from quivr_api.modules.sync.entity.sync_models import (
    DBSyncFile,
    DownloadedSyncFile,
    SyncFile,
    SyncsActive,
    SyncsUser,
)
from quivr_api.modules.sync.repository.sync_files import SyncFilesRepository
from quivr_api.modules.sync.service.sync_service import SyncService, SyncUserService
from quivr_api.modules.sync.utils.sync import BaseSync
from quivr_api.modules.upload.service.upload_file import (
    check_file_exists,
    upload_file_storage,
)

logger = get_logger(__name__)

celery_inspector = celery.control.inspect()


# NOTE: we are filtering based on file path names in sync  !
def filter_on_supported_files(
    files: list[SyncFile], existing_files: dict[str, DBSyncFile]
) -> list[Tuple[SyncFile, DBSyncFile | None]]:
    res = []
    for new_file in files:
        prev_file = existing_files.get(new_file.name, None)
        if (prev_file and prev_file.supported) or prev_file is None:
            res.append((new_file, prev_file))

    return res


def should_download_file(
    file: SyncFile,
    last_synced_time: datetime | None,
    provider_name: str,
    brain_id: UUID,
    datetime_format: str,
) -> bool:
    file_last_modified_utc = datetime.strptime(
        file.last_modified, datetime_format
    ).replace(tzinfo=timezone.utc)

    should_download = not last_synced_time or file_last_modified_utc > last_synced_time
    should_download &= not check_file_exists(str(brain_id), file.name)

    if provider_name == "notion":
        should_download &= file.mime_type != "db"
    else:
        should_download &= not file.is_folder

    return should_download


class SyncUtils:
    def __init__(
        self,
        sync_user_service: SyncUserService,
        sync_active_service: SyncService,
        knowledge_service: KnowledgeService,
        sync_files_repo: SyncFilesRepository,
        storage: Storage,
        sync_cloud: BaseSync,
        notification_service: NotificationService,
        brain_vectors: BrainsVectors,
    ) -> None:
        self.sync_user_service = sync_user_service
        self.sync_active_service = sync_active_service
        self.knowledge_service = knowledge_service
        self.sync_files_repo = sync_files_repo
        self.storage = storage
        self.sync_cloud = sync_cloud
        self.notification_service = notification_service
        self.brain_vectors = brain_vectors

    def create_sync_bulk_notification(
        self, files: list[SyncFile], current_user: UUID, brain_id: UUID, bulk_id: UUID
    ) -> list[SyncFile]:
        res = []
        # TODO: bulk insert in batch
        for file in files:
            upload_notification = self.notification_service.add_notification(
                CreateNotification(
                    user_id=current_user,
                    bulk_id=bulk_id,
                    status=NotificationsStatusEnum.INFO,
                    title=file.name,
                    category="sync",
                    brain_id=str(brain_id),
                )
            )
            file.notification_id = upload_notification.id
            res.append(file)
        return res

    def download_file(
        self, file: SyncFile, credentials: dict[str, Any]
    ) -> DownloadedSyncFile:
        logger.info(f"Downloading {file} using {self.sync_cloud}")
        file_response = self.sync_cloud.download_file(credentials, file)
        logger.debug(f"Fetch sync file response: {file_response}")
        file_name = str(file_response["file_name"])
        raw_data = file_response["content"]
        file_data = (
            io.BufferedReader(raw_data)  # type: ignore
            if isinstance(raw_data, io.BytesIO)
            else io.BufferedReader(raw_data.encode("utf-8"))  # type: ignore
        )

        extension = os.path.splitext(file_name)[-1].lower()
        dfile = DownloadedSyncFile(
            file_name=file_name, file_data=file_data, extension=extension
        )
        logger.debug(f"Successfully downloded sync file : {dfile}")
        return dfile

    async def process_sync_file(
        self,
        client: AsyncClient,
        file: SyncFile,
        previous_file: DBSyncFile | None,
        current_user: SyncsUser,
        sync_active: SyncsActive,
    ):
        logger.info("Processing file: %s", file.name)
        brain_id = sync_active.brain_id
        integration, integration_link = self.sync_cloud.name, file.web_view_link
        downloaded_file = self.download_file(file, current_user.credentials)

        if downloaded_file.extension not in [
            ".pdf",
            ".txt",
            ".md",
            ".csv",
            ".docx",
            ".xlsx",
            ".pptx",
            ".doc",
        ]:
            raise ValueError(f"Incompatible file extension for {downloaded_file}")

        # TODO: Check workflow is correct
        # FIXME(@aminediro, @chloedia): Checks should use file_sha1 in database
        if check_file_exists(str(brain_id), downloaded_file.file_name):
            self.brain_vectors.delete_file_from_brain(
                brain_id, downloaded_file.file_name
            )

        # TODO(@aminediro):  check_user_limits()
        # TODO(@chloedia) : change with knowledge_id
        # FILE Extension should be field
        # Upload File to S3 Storage
        storage_path = str(brain_id) + "/" + downloaded_file.file_name
        response = await upload_file_storage(
            client,
            downloaded_file.file_data,
            storage_path,
            upsert=(previous_file is not None),
        )

        assert response, f"Error uploading {downloaded_file} to  {storage_path}"
        self.notification_service.update_notification_by_id(
            file.notification_id,
            NotificationUpdatableProperties(
                status=NotificationsStatusEnum.SUCCESS,
                description="File downloaded successfully",
            ),
        )
        knowledge_to_add = CreateKnowledgeProperties(
            brain_id=brain_id,
            file_name=file.name,
            extension=downloaded_file.extension,
            integration=integration,
            integration_link=integration_link,
        )

        added_knowledge = self.knowledge_service.add_knowledge(knowledge_to_add)
        # Send file for processing
        celery.send_task(
            "process_file_task",
            kwargs={
                "brain_id": brain_id,
                "knowledge_id": added_knowledge.id,
                "file_name": storage_path,
                "file_original_name": file.name,
                "integration": integration,
                "integration_link": integration_link,
                "notification_id": file.notification_id,
            },
        )
        self.sync_files_repo.update_or_create_sync_file(
            file=file,
            previous_file=previous_file,
            sync_active=sync_active,
            supported=True,
        )
        return file

    async def process_sync_diff(
        self,
        files: List[SyncFile],
        current_user: SyncsUser,
        sync_active: SyncsActive,
    ):
        """
        Download files from an external cloud.

        Args:
            credentials (dict): The token data for accessing the external cloud.
            files (list): The list of file metadata to download.

        Returns:
            dict: A dictionary containing the status of the download or an error message.
        """

        # TODO: Inject client
        aclient = await get_supabase_async_client()
        current_user.credentials = self.sync_cloud.check_and_refresh_access_token(
            current_user.credentials
        )

        bulk_id = uuid4()
        downloaded_files = []
        list_existing_files = self.sync_files_repo.get_sync_files(sync_active.id)
        existing_files = {f.path: f for f in list_existing_files}

        supported_files = filter_on_supported_files(files, existing_files)

        files = self.create_sync_bulk_notification(
            files, current_user.user_id, sync_active.brain_id, bulk_id
        )

        for file, prev_file in supported_files:
            try:
                result = await self.process_sync_file(
                    file=file,
                    previous_file=prev_file,
                    client=aclient,
                    current_user=current_user,
                    sync_active=sync_active,
                )
                if result is not None:
                    downloaded_files.append(result)

                self.notification_service.update_notification_by_id(
                    file.notification_id,
                    NotificationUpdatableProperties(
                        status=NotificationsStatusEnum.SUCCESS,
                        description="File downloaded successfully",
                    ),
                )

            except Exception as e:
                logger.error(
                    "An error occurred while downloading %s files: %s",
                    self.sync_cloud.name,
                    e,
                )
                # NOTE: Supported is  True
                self.sync_files_repo.update_or_create_sync_file(
                    file=file,
                    sync_active=sync_active,
                    previous_file=prev_file,
                    supported=False,
                )
                self.notification_service.update_notification_by_id(
                    file.notification_id,
                    NotificationUpdatableProperties(
                        status=NotificationsStatusEnum.ERROR,
                        description="Error downloading file",
                    ),
                )

        return {"downloaded_files": downloaded_files}

    async def get_files_to_download(
        self, sync_active: SyncsActive, user_sync: SyncsUser
    ) -> list[SyncFile]:
        # Get the folder id from the settings from sync_active
        folders = sync_active.settings.get("folders", [])
        files_to_download = sync_active.settings.get("files", [])
        files: List[SyncFile] = []
        files_metadata = []

        if self.sync_cloud.lower_name == "notion":
            files += folders

        # TODO: can be done in parallel
        for folder in folders:
            files.extend(
                await self.sync_cloud.aget_files(
                    user_sync.credentials,
                    folder_id=folder,
                    recursive=True,
                )
            )
        if len(files_to_download) > 0:
            files_metadata = await self.sync_cloud.aget_files_by_id(
                user_sync.credentials,
                files_to_download,
            )
        files = files + files_metadata
        logger.debug(f"original files to download for {sync_active.id} : {files}")

        # Filter files that have been modified since the last sync
        # TODO: what is this ????
        last_synced_time = (
            datetime.fromisoformat(sync_active.last_synced).astimezone(timezone.utc)
            if sync_active.last_synced
            else None
        )

        files_to_download = [
            file
            for file in files
            if should_download_file(
                file=file,
                last_synced_time=last_synced_time,
                provider_name=self.sync_cloud.lower_name,
                datetime_format=self.sync_cloud.datetime_format,
                brain_id=sync_active.brain_id,
            )
        ]

        logger.debug(
            f"filter files to download for {sync_active} : {files_to_download}"
        )
        return files_to_download

    async def sync(
        self,
        sync_active: SyncsActive,
        user_sync: SyncsUser,
    ):
        """
        Check if the Specific sync has not been synced and download the folders and files based on the settings.

        Args:
            sync_active_id (int): The ID of the active sync.
            user_id (str): The user ID associated with the active sync.
        """
        logger.info(
            "Starting  %s sync for sync_active: %s",
            self.sync_cloud.lower_name,
            sync_active,
        )

        files_to_download = await self.get_files_to_download(sync_active, user_sync)
        processed_files = await self.process_sync_diff(
            files=files_to_download,
            current_user=user_sync,
            sync_active=sync_active,
        )

        # Update the last_synced timestamp
        self.sync_active_service.update_sync_active(
            sync_active.id,
            SyncsActiveUpdateInput(
                last_synced=datetime.now().astimezone().isoformat(), force_sync=False
            ),
        )
        logger.info(
            f"{self.sync_cloud.lower_name} sync completed for sync_active: {sync_active.id}. Synced all {len(processed_files)} files.",
        )
        return processed_files
