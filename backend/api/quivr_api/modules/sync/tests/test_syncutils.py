from datetime import datetime, timedelta, timezone
from typing import Tuple
from uuid import uuid4

import pytest

from quivr_api.modules.brain.entity.brain_entity import Brain
from quivr_api.modules.notification.entity.notification import NotificationsStatusEnum
from quivr_api.modules.sync.entity.sync_models import (
    DBSyncFile,
    SyncFile,
    SyncsActive,
    SyncsUser,
)
from quivr_api.modules.sync.utils.syncutils import (
    SyncUtils,
    filter_on_supported_files,
    should_download_file,
)
from quivr_api.modules.upload.service.upload_file import check_file_exists
from quivr_api.modules.user.entity.user_identity import User


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


@pytest.mark.asyncio(loop_scope="session")
async def test_get_syncfiles_from_ids_nofolder(syncutils: SyncUtils):
    files = await syncutils.get_syncfiles_from_ids(
        credentials={}, files_ids=[str(uuid4())], folder_ids=[], sync_user_id=1
    )
    assert len(files) == 1


@pytest.mark.asyncio(loop_scope="session")
async def test_get_syncfiles_from_ids_folder(syncutils: SyncUtils):
    files = await syncutils.get_syncfiles_from_ids(
        credentials={},
        files_ids=[str(uuid4())],
        folder_ids=[str(uuid4())],
        sync_user_id=0,
    )
    assert len(files) == 2


@pytest.mark.asyncio(loop_scope="session")
async def test_get_syncfiles_from_ids_notion(syncutils_notion: SyncUtils):
    files = await syncutils_notion.get_syncfiles_from_ids(
        credentials={},
        files_ids=[str(uuid4())],
        folder_ids=[str(uuid4())],
        sync_user_id=0,
    )
    assert len(files) == 3


@pytest.mark.asyncio(loop_scope="session")
async def test_download_file(syncutils: SyncUtils):
    file = SyncFile(
        id=str(uuid4()),
        name="test_file.txt",
        is_folder=False,
        last_modified=datetime.now().strftime(syncutils.sync_cloud.datetime_format),
        mime_type="txt",
        web_view_link="",
    )
    dfile = await syncutils.download_file(file, {})
    assert dfile.extension == ".txt"
    assert dfile.file_name == file.name
    assert len(dfile.file_data.read()) > 0


@pytest.mark.asyncio(loop_scope="session")
async def test_process_sync_file_not_supported(syncutils: SyncUtils):
    file = SyncFile(
        id=str(uuid4()),
        name="test_file.asldkjfalsdkjf",
        is_folder=False,
        last_modified=datetime.now().strftime(syncutils.sync_cloud.datetime_format),
        mime_type="txt",
        web_view_link="",
        notification_id=uuid4(),  #
    )
    brain_id = uuid4()
    sync_user = SyncsUser(
        id=1,
        user_id=uuid4(),
        name="c8xfz3g566b8xa1ajiesdh",
        provider="mock",
        credentials={},
        state={},
        additional_data={},
        status="",
    )
    sync_active = SyncsActive(
        id=1,
        name="test",
        syncs_user_id=1,
        user_id=sync_user.user_id,
        settings={},
        last_synced=str(datetime.now() - timedelta(hours=5)),
        sync_interval_minutes=1,
        brain_id=brain_id,
    )

    with pytest.raises(ValueError):
        await syncutils.process_sync_file(
            file=file,
            previous_file=None,
            current_user=sync_user,
            sync_active=sync_active,
        )


@pytest.mark.skip(
    reason="Bug: UnboundLocalError: cannot access local variable 'response'"
)
@pytest.mark.asyncio(loop_scope="session")
async def test_process_sync_file_noprev(
    monkeypatch,
    brain_user_setup: Tuple[Brain, User],
    setup_syncs_data: Tuple[SyncsUser, SyncsActive],
    syncutils: SyncUtils,
    sync_file: SyncFile,
):
    task = {}

    def _send_task(*args, **kwargs):
        task["args"] = args
        task["kwargs"] = {**kwargs["kwargs"]}

    monkeypatch.setattr("quivr_api.celery_config.celery.send_task", _send_task)

    brain_1, _ = brain_user_setup
    assert brain_1.brain_id
    (sync_user, sync_active) = setup_syncs_data
    await syncutils.process_sync_file(
        file=sync_file,
        previous_file=None,
        current_user=sync_user,
        sync_active=sync_active,
    )

    # Check notification inserted
    assert (
        sync_file.notification_id in syncutils.notification_service.repository.received  # type: ignore
    )
    assert (
        syncutils.notification_service.repository.received[  # type: ignore
            sync_file.notification_id  # type: ignore
        ].status
        == NotificationsStatusEnum.SUCCESS
    )

    # Check Syncfile created
    dbfiles: list[DBSyncFile] = syncutils.sync_files_repo.get_sync_files(sync_active.id)
    assert len(dbfiles) == 1
    assert dbfiles[0].brain_id == str(brain_1.brain_id)
    assert dbfiles[0].syncs_active_id == sync_active.id
    assert dbfiles[0].supported

    # Check knowledge created
    all_km = await syncutils.knowledge_service.get_all_knowledge_in_brain(
        brain_1.brain_id
    )
    assert len(all_km) == 1
    created_km = all_km[0]
    assert created_km.file_name == sync_file.name
    assert created_km.extension == ".txt"
    assert created_km.file_sha1 is None
    assert created_km.created_at is not None
    assert created_km.metadata == {"sync_file_id": "1"}
    assert len(created_km.brains) > 0
    assert created_km.brains[0]["brain_id"] == brain_1.brain_id

    # Assert celery task in correct
    assert task["args"] == ("process_file_task",)
    minimal_task_kwargs = {
        "brain_id": brain_1.brain_id,
        "knowledge_id": created_km.id,
        "file_original_name": sync_file.name,
        "source": syncutils.sync_cloud.name,
        "notification_id": sync_file.notification_id,
    }
    all(
        minimal_task_kwargs[key] == task["kwargs"][key]  # type: ignore
        for key in minimal_task_kwargs
    )


@pytest.mark.skip(
    reason="Bug: UnboundLocalError: cannot access local variable 'response'"
)
@pytest.mark.asyncio(loop_scope="session")
async def test_process_sync_file_with_prev(
    monkeypatch,
    supabase_client,
    brain_user_setup: Tuple[Brain, User],
    setup_syncs_data: Tuple[SyncsUser, SyncsActive],
    syncutils: SyncUtils,
    sync_file: SyncFile,
    prev_file: SyncFile,
):
    task = {}

    def _send_task(*args, **kwargs):
        task["args"] = args
        task["kwargs"] = {**kwargs["kwargs"]}

    monkeypatch.setattr("quivr_api.celery_config.celery.send_task", _send_task)
    brain_1, _ = brain_user_setup
    assert brain_1.brain_id
    (sync_user, sync_active) = setup_syncs_data

    # Run process_file on prev_file first
    await syncutils.process_sync_file(
        file=prev_file,
        previous_file=None,
        current_user=sync_user,
        sync_active=sync_active,
    )
    dbfiles: list[DBSyncFile] = syncutils.sync_files_repo.get_sync_files(sync_active.id)
    assert len(dbfiles) == 1
    prev_dbfile = dbfiles[0]

    assert check_file_exists(str(brain_1.brain_id), prev_file.name)
    prev_file_data = supabase_client.storage.from_("quivr").download(
        f"{brain_1.brain_id}/{prev_file.name}"
    )

    #####
    # Run process_file on newer file
    await syncutils.process_sync_file(
        file=sync_file,
        previous_file=prev_dbfile,
        current_user=sync_user,
        sync_active=sync_active,
    )

    # Check notification inserted
    assert (
        sync_file.notification_id in syncutils.notification_service.repository.received  # type: ignore
    )
    assert (
        syncutils.notification_service.repository.received[  # type: ignore
            sync_file.notification_id  # type: ignore
        ].status
        == NotificationsStatusEnum.SUCCESS
    )

    # Check Syncfile created
    dbfiles: list[DBSyncFile] = syncutils.sync_files_repo.get_sync_files(sync_active.id)
    assert len(dbfiles) == 1
    assert dbfiles[0].brain_id == str(brain_1.brain_id)
    assert dbfiles[0].syncs_active_id == sync_active.id
    assert dbfiles[0].supported

    # Check prev file was deleted and replaced with the new
    all_km = await syncutils.knowledge_service.get_all_knowledge_in_brain(
        brain_1.brain_id
    )
    assert len(all_km) == 1
    created_km = all_km[0]
    assert created_km.file_name == sync_file.name
    assert created_km.extension == ".txt"
    assert created_km.file_sha1 is None
    assert created_km.updated_at
    assert created_km.created_at
    assert created_km.updated_at == created_km.created_at  # new line
    assert created_km.metadata == {"sync_file_id": str(dbfiles[0].id)}
    assert created_km.brains[0]["brain_id"] == brain_1.brain_id

    # Check file content changed
    assert check_file_exists(str(brain_1.brain_id), sync_file.name)
    new_file_data = supabase_client.storage.from_("quivr").download(
        f"{brain_1.brain_id}/{sync_file.name}"
    )
    assert new_file_data != prev_file_data, "Same file in prev_file and new file"

    # Assert celery task in correct
    assert task["args"] == ("process_file_task",)
    minimal_task_kwargs = {
        "brain_id": brain_1.brain_id,
        "knowledge_id": created_km.id,
        "file_original_name": sync_file.name,
        "source": syncutils.sync_cloud.name,
        "notification_id": sync_file.notification_id,
    }
    all(
        minimal_task_kwargs[key] == task["kwargs"][key]  # type: ignore
        for key in minimal_task_kwargs
    )
