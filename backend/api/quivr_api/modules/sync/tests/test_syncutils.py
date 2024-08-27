from datetime import datetime, timedelta, timezone
from uuid import uuid4

import pytest

from quivr_api.modules.sync.entity.sync_models import (
    DBSyncFile,
    SyncFile,
)
from quivr_api.modules.sync.utils.syncutils import (
    SyncUtils,
    filter_on_supported_files,
    should_download_file,
)


def test_filter_on_supported_files_empty_existing():
    files = [
        SyncFile(
            id="1",
            name="file_name",
            is_folder=True,
            last_modified=str(datetime.now()),
            mime_type="txt",
            web_view_link="link",
        )
    ]
    existing_file = {}

    assert [(files[0], None)] == filter_on_supported_files(files, existing_file)


def test_filter_on_supported_files_prev_not_supported():
    files = [
        SyncFile(
            id=f"{idx}",
            name=f"file_name_{idx}",
            is_folder=False,
            last_modified=str(datetime.now()),
            mime_type="txt",
            web_view_link="link",
        )
        for idx in range(3)
    ]
    existing_files = {
        file.name: DBSyncFile(
            id=idx,
            path=file.name,
            syncs_active_id=1,
            last_modified=str(datetime.now()),
            brain_id=str(uuid4()),
            supported=idx % 2 == 0,
        )
        for idx, file in enumerate(files)
    }

    assert [
        (files[idx], existing_files[f"file_name_{idx}"])
        for idx in range(3)
        if idx % 2 == 0
    ] == filter_on_supported_files(files, existing_files)


def test_should_download_file_no_sync_time_not_folder():
    datetime_format: str = "%Y-%m-%dT%H:%M:%S.%fZ"
    file_not_folder = SyncFile(
        id="1",
        name="file_name",
        is_folder=False,
        last_modified=datetime.now().strftime(datetime_format),
        mime_type="txt",
        web_view_link="link",
    )
    assert should_download_file(
        file=file_not_folder,
        last_updated_sync_active=None,
        provider_name="google",
        datetime_format=datetime_format,
    )


def test_should_download_file_no_sync_time_folder():
    datetime_format: str = "%Y-%m-%dT%H:%M:%S.%fZ"
    file_not_folder = SyncFile(
        id="1",
        name="file_name",
        is_folder=True,
        last_modified=datetime.now().strftime(datetime_format),
        mime_type="txt",
        web_view_link="link",
    )
    assert not should_download_file(
        file=file_not_folder,
        last_updated_sync_active=None,
        provider_name="google",
        datetime_format=datetime_format,
    )


def test_should_download_file_notiondb():
    datetime_format: str = "%Y-%m-%dT%H:%M:%S.%fZ"
    file_not_folder = SyncFile(
        id="1",
        name="file_name",
        is_folder=False,
        last_modified=datetime.now().strftime(datetime_format),
        mime_type="db",
        web_view_link="link",
    )

    assert not should_download_file(
        file=file_not_folder,
        last_updated_sync_active=(datetime.now() - timedelta(hours=5)).astimezone(
            timezone.utc
        ),
        provider_name="notion",
        datetime_format=datetime_format,
    )


def test_should_download_file_not_notiondb():
    datetime_format: str = "%Y-%m-%dT%H:%M:%S.%fZ"
    file_not_folder = SyncFile(
        id="1",
        name="file_name",
        is_folder=False,
        last_modified=datetime.now().strftime(datetime_format),
        mime_type="md",
        web_view_link="link",
    )

    assert should_download_file(
        file=file_not_folder,
        last_updated_sync_active=None,
        provider_name="notion",
        datetime_format=datetime_format,
    )


def test_should_download_file_lastsynctime_before():
    datetime_format: str = "%Y-%m-%dT%H:%M:%S.%fZ"
    file_not_folder = SyncFile(
        id="1",
        name="file_name",
        is_folder=False,
        last_modified=datetime.now().strftime(datetime_format),
        mime_type="txt",
        web_view_link="link",
    )
    last_sync_time = (datetime.now() - timedelta(hours=5)).astimezone(timezone.utc)

    assert should_download_file(
        file=file_not_folder,
        last_updated_sync_active=last_sync_time,
        provider_name="google",
        datetime_format=datetime_format,
    )


def test_should_download_file_lastsynctime_after():
    datetime_format: str = "%Y-%m-%dT%H:%M:%S.%fZ"
    file_not_folder = SyncFile(
        id="1",
        name="file_name",
        is_folder=False,
        last_modified=(datetime.now() - timedelta(hours=5)).strftime(datetime_format),
        mime_type="txt",
        web_view_link="link",
    )
    last_sync_time = datetime.now().astimezone(timezone.utc)

    assert not should_download_file(
        file=file_not_folder,
        last_updated_sync_active=last_sync_time,
        provider_name="google",
        datetime_format=datetime_format,
    )


class TestSyncUtils:
    @pytest.mark.asyncio
    async def test_get_syncfiles_from_ids_nofolder(self, syncutils: SyncUtils):
        files = await syncutils.get_syncfiles_from_ids(
            credentials={}, files_ids=[str(uuid4())], folder_ids=[]
        )
        assert len(files) == 1

    @pytest.mark.asyncio
    async def test_get_syncfiles_from_ids_folder(self, syncutils: SyncUtils):
        files = await syncutils.get_syncfiles_from_ids(
            credentials={}, files_ids=[str(uuid4())], folder_ids=[str(uuid4())]
        )
        assert len(files) == 2

    @pytest.mark.asyncio
    async def test_get_syncfiles_from_ids_notion(self, syncutils_notion: SyncUtils):
        files = await syncutils_notion.get_syncfiles_from_ids(
            credentials={}, files_ids=[str(uuid4())], folder_ids=[str(uuid4())]
        )
        assert len(files) == 3
