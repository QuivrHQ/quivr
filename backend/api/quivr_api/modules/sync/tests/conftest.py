import json
import os
from collections import defaultdict
from datetime import datetime, timedelta
from io import BytesIO
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union
from uuid import UUID, uuid4

import pytest
import pytest_asyncio
from sqlmodel import select

from quivr_api.modules.brain.entity.brain_entity import Brain, BrainType
from quivr_api.modules.brain.repository.brains_vectors import BrainsVectors
from quivr_api.modules.knowledge.repository.knowledges import KnowledgeRepository
from quivr_api.modules.knowledge.service.knowledge_service import KnowledgeService
from quivr_api.modules.notification.dto.inputs import (
    CreateNotification,
    NotificationUpdatableProperties,
)
from quivr_api.modules.notification.entity.notification import (
    Notification,
    NotificationsStatusEnum,
)
from quivr_api.modules.notification.repository.notifications_interface import (
    NotificationInterface,
)
from quivr_api.modules.notification.service.notification_service import (
    NotificationService,
)
from quivr_api.modules.sync.dto.inputs import (
    SyncFileInput,
    SyncFileUpdateInput,
    SyncsActiveInput,
    SyncsActiveUpdateInput,
    SyncsUserInput,
    SyncUserUpdateInput,
)
from quivr_api.modules.sync.entity.notion_page import (
    BlockParent,
    DatabaseParent,
    NotionPage,
    NotionSearchResult,
    PageParent,
    PageProps,
    TextContent,
    Title,
    TitleItem,
    WorkspaceParent,
)
from quivr_api.modules.sync.entity.sync_models import (
    DBSyncFile,
    SyncFile,
    SyncsActive,
    SyncsUser,
)
from quivr_api.modules.sync.repository.sync_interfaces import SyncFileInterface
from quivr_api.modules.sync.service.sync_notion import SyncNotionService
from quivr_api.modules.sync.service.sync_service import (
    ISyncService,
    ISyncUserService,
)
from quivr_api.modules.sync.utils.sync import (
    BaseSync,
)
from quivr_api.modules.sync.utils.syncutils import (
    SyncUtils,
)
from quivr_api.modules.user.entity.user_identity import User

pg_database_base_url = "postgres:postgres@localhost:54322/postgres"


@pytest.fixture(scope="function")
def page_response() -> dict[str, Any]:
    json_path = (
        Path(os.getenv("PYTEST_CURRENT_TEST").split(":")[0])
        .parent.absolute()
        .joinpath("page.json")
    )
    with open(json_path, "r") as f:
        page = json.load(f)
    return page


@pytest.fixture(scope="function")
def fetch_response():
    return [
        {
            "object": "page",
            "id": "27b26c5a-e86f-470a-a5fc-27a3fc308850",
            "created_time": "2024-05-02T09:03:00.000Z",
            "last_edited_time": "2024-08-19T10:01:00.000Z",
            "created_by": {
                "object": "user",
                "id": "e2f8bfda-3b98-466e-a2c1-39e5f0f64881",
            },
            "last_edited_by": {
                "object": "user",
                "id": "f87bcc4b-68ee-4d44-b518-3d2d19ffedc2",
            },
            "cover": None,
            "icon": {"type": "emoji", "emoji": "🌇"},
            "parent": {"type": "workspace", "workspace": True},
            "archived": False,
            "in_trash": False,
            "properties": {
                "title": {
                    "id": "title",
                    "type": "title",
                    "title": [
                        {
                            "type": "text",
                            "text": {"content": "Investors", "link": None},
                            "annotations": {
                                "bold": False,
                                "italic": False,
                                "strikethrough": False,
                                "underline": False,
                                "code": False,
                                "color": "default",
                            },
                            "plain_text": "Investors",
                            "href": None,
                        }
                    ],
                }
            },
            "url": "https://www.notion.so/Investors-27b26c5ae86f470aa5fc27a3fc308850",
            "public_url": None,
        },
        {
            "object": "page",
            "id": "ff799030-eae6-4c81-8631-ee2653f27af8",
            "created_time": "2024-04-04T23:24:00.000Z",
            "last_edited_time": "2024-08-19T10:01:00.000Z",
            "created_by": {
                "object": "user",
                "id": "c8de6079-cc5a-4b46-8763-04f92b33fc18",
            },
            "last_edited_by": {
                "object": "user",
                "id": "f87bcc4b-68ee-4d44-b518-3d2d19ffedc2",
            },
            "cover": None,
            "icon": {"type": "emoji", "emoji": "🎓"},
            "parent": {"type": "workspace", "workspace": True},
            "archived": False,
            "in_trash": False,
            "properties": {
                "title": {
                    "id": "title",
                    "type": "title",
                    "title": [
                        {
                            "type": "text",
                            "text": {"content": "Academy", "link": None},
                            "annotations": {
                                "bold": False,
                                "italic": False,
                                "strikethrough": False,
                                "underline": False,
                                "code": False,
                                "color": "default",
                            },
                            "plain_text": "Academy",
                            "href": None,
                        }
                    ],
                }
            },
            "url": "https://www.notion.so/Academy-ff799030eae64c818631ee2653f27af8",
            "public_url": None,
        },
    ]


@pytest.fixture
def search_result():
    return [
        {
            "object": "page",
            "id": "77b34b29-96f5-487c-b594-ba69cbb951c0",
            "created_time": "2024-07-29T16:58:00.000Z",
            "last_edited_time": "2024-07-30T07:46:00.000Z",
            "created_by": {
                "object": "user",
                "id": "c8de6079-cc5a-4b46-8763-04f92b33fc18",
            },
            "last_edited_by": {
                "object": "user",
                "id": "c8de6079-cc5a-4b46-8763-04f92b33fc18",
            },
            "cover": None,
            "icon": {"type": "emoji", "emoji": ":brain:"},
            "parent": {
                "type": "page_id",
                "page_id": "6df769b6-3849-4141-b61c-14f0f6d4fa43",
            },
            "archived": False,
            "in_trash": False,
            "properties": {
                "title": {
                    "id": "title",
                    "type": "title",
                    "title": [
                        {
                            "type": "text",
                            "text": {"content": "MEDDPICC", "link": None},
                            "annotations": {
                                "bold": False,
                                "italic": False,
                                "strikethrough": False,
                                "underline": False,
                                "code": False,
                                "color": "default",
                            },
                            "plain_text": "MEDDPICC",
                            "href": None,
                        }
                    ],
                }
            },
            "url": "https://www.notion.so/MEDDPICC-77b34b2996f5487cb594ba69cbb951c0",
            "public_url": None,
        }
    ]


@pytest.fixture(scope="function")
def user_1(sync_session) -> User:
    user_1 = (
        sync_session.exec(select(User).where(User.email == "admin@quivr.app"))
    ).one()
    return user_1


@pytest.fixture(
    params=[
        PageParent(type="page_id", page_id=uuid4()),
        WorkspaceParent(type="workspace", workspace=True),
    ]
)
def notion_search_result(request) -> NotionSearchResult:
    return NotionSearchResult(
        results=[
            NotionPage(
                id=uuid4(),
                created_time=datetime.now(),
                last_edited_time=datetime.now(),
                url="url",
                archived=False,
                in_trash=False,
                public_url=None,
                parent=request.param,
                cover=None,
                icon=None,
                properties=PageProps(
                    title=Title(
                        id="id_title",
                        type="title",
                        title=[
                            TitleItem(
                                type="text",
                                text=TextContent(
                                    content="title",
                                    link=None,
                                ),
                                annotations={},
                                plain_text="",
                            )
                        ],
                    )
                ),
            )
        ],
        has_more=False,
        next_cursor=None,
    )


@pytest.fixture(
    params=[
        DatabaseParent(type="database_id", database_id=uuid4()),
        BlockParent(type="block_id", block_id=uuid4()),
    ]
)
def notion_search_result_bad_parent(request) -> NotionSearchResult:
    return NotionSearchResult(
        results=[
            NotionPage(
                id=uuid4(),
                created_time=datetime.now(),
                last_edited_time=datetime.now(),
                url="url",
                archived=False,
                in_trash=False,
                public_url=None,
                parent=request.param,
                cover=None,
                icon=None,
                properties=PageProps(
                    title=Title(
                        id="id_title",
                        type="title",
                        title=[
                            TitleItem(
                                type="text",
                                text=TextContent(
                                    content="title",
                                    link=None,
                                ),
                                annotations={},
                                plain_text="",
                            )
                        ],
                    )
                ),
            )
        ],
        has_more=False,
        next_cursor=None,
    )


class MockSyncCloud(BaseSync):
    # TODO: Mock notion
    name = "mockcloud"
    lower_name = "mockcloud"
    datetime_format: str = "%Y-%m-%d %H:%M:%S"

    def get_files_by_id(self, credentials: Dict, file_ids: List[str]) -> List[SyncFile]:
        raise NotImplementedError

    def get_files(
        self, credentials: Dict, folder_id: str | None = None, recursive: bool = False
    ) -> List[SyncFile]:
        raise NotImplementedError()

    def download_file(
        self, credentials: Dict, file: SyncFile
    ) -> Dict[str, Union[str, BytesIO]]:
        raise NotImplementedError

    # Implement async only
    async def aget_files_by_id(
        self, credentials: Dict, file_ids: List[str]
    ) -> List[SyncFile]:
        return [
            SyncFile(
                id=fid,
                name=f"file_{fid}",
                is_folder=False,
                last_modified=datetime.now().strftime(self.datetime_format),
                mime_type="txt",
                web_view_link=f"{self.name}/{fid}",
            )
            for fid in file_ids
        ]

    async def aget_files(
        self, credentials: Dict, folder_id: str | None = None, recursive: bool = False
    ) -> List[SyncFile]:
        n_files = 1
        return [
            SyncFile(
                id=str(uuid4()),
                name=f"file_in_{folder_id}",
                is_folder=False,
                last_modified=datetime.now().strftime(self.datetime_format),
                mime_type="txt",
                web_view_link=f"{self.name}/{fid}",
            )
            for fid in range(n_files)
        ]

    async def adownload_file(
        self, credentials: Dict, file: SyncFile
    ) -> Dict[str, Union[str, BytesIO]]:
        return {"file_name": file.name, "content": BytesIO(os.urandom(128))}

    def check_and_refresh_access_token(self, credentials: dict) -> Dict:
        return credentials


class MockSyncCloudNotion(MockSyncCloud):
    # TODO: Mock notion
    name = "notion"
    lower_name = "notion"
    datetime_format: str = "%Y-%m-%d %H:%M:%S"


class MockNotification(NotificationInterface):
    def __init__(
        self,
        notification_ids: list[UUID],
        user_id: UUID,
        brain_id: UUID,
    ):
        self.received: dict[UUID, Notification] = {}
        for notification_id in notification_ids:
            self.received[notification_id] = Notification(
                id=notification_id,
                user_id=user_id,
                status=NotificationsStatusEnum.INFO,
                category="sync",
                title="test",
                description="",
                datetime=datetime.now(),
                brain_id=str(brain_id),
            )

    def add_notification(self, notification: CreateNotification) -> Notification:
        notif = Notification(
            datetime=datetime.now(), id=uuid4(), **notification.model_dump()
        )
        self.received[notif.id] = notif
        return notif

    def update_notification_by_id(
        self, notification_id: UUID, notification: NotificationUpdatableProperties
    ) -> Notification:
        prev_notif = self.received[notification_id]
        prev_notif = Notification(
            **{**prev_notif.model_dump(), **notification.model_dump()}
        )
        self.received[notification_id] = prev_notif
        return prev_notif

    def remove_notification_by_id(self, notification_id: UUID):
        del self.received[notification_id]


class MockSyncService(ISyncService):
    def __init__(self, sync_active: SyncsActive):
        self.syncs_active_user = {}
        self.syncs_active_id = {}
        self.syncs_active_user[sync_active.user_id] = sync_active
        self.syncs_active_id[sync_active.id] = sync_active

    def create_sync_active(
        self,
        sync_active_input: SyncsActiveInput,
        user_id: str,
    ) -> SyncsActive | None:
        sactive = SyncsActive(
            id=len(self.syncs_active_user) + 1,
            user_id=UUID(user_id),
            **sync_active_input.model_dump(),
        )
        self.syncs_active_user[user_id] = sactive
        return sactive

    def get_syncs_active(self, user_id: str) -> List[SyncsActive]:
        return self.syncs_active_user[user_id]

    def update_sync_active(
        self, sync_id: int, sync_active_input: SyncsActiveUpdateInput
    ):
        sync = self.syncs_active_id[sync_id]
        sync = SyncsActive(**sync.model_dump(), **sync_active_input.model_dump())
        self.syncs_active_id[sync_id] = sync
        return sync

    def delete_sync_active(self, sync_active_id: int, user_id: UUID):
        del self.syncs_active_id[sync_active_id]
        del self.syncs_active_user[user_id]

    async def get_syncs_active_in_interval(self) -> List[SyncsActive]:
        return list(self.syncs_active_id.values())

    def get_details_sync_active(self, sync_active_id: int):
        return


class MockSyncUserService(ISyncUserService):
    def __init__(self, sync_user: SyncsUser):
        self.map_id = {}
        self.map_userid = {}
        self.map_id[sync_user.id] = sync_user
        self.map_userid[sync_user.id] = sync_user

    def get_syncs_user(self, user_id: UUID, sync_user_id: int | None = None):
        return self.map_userid[user_id]

    def get_sync_user_by_id(self, sync_id: int):
        return self.map_id[sync_id]

    def create_sync_user(self, sync_user_input: SyncsUserInput):
        id = len(self.map_userid) + 1
        self.map_userid[sync_user_input.user_id] = SyncsUser(
            id=id, **sync_user_input.model_dump()
        )
        self.map_id[id] = self.map_userid[sync_user_input.user_id]
        return self.map_id[id]

    def delete_sync_user(self, sync_id: int, user_id: str):
        del self.map_userid[user_id]
        del self.map_userid[sync_id]

    def get_sync_user_by_state(self, state: dict) -> SyncsUser | None:
        return list(self.map_userid.values())[-1]

    def update_sync_user(
        self, sync_user_id: UUID, state: dict, sync_user_input: SyncUserUpdateInput
    ):
        return

    def get_all_notion_user_syncs(self):
        return

    async def get_files_folder_user_sync(
        self,
        sync_active_id: int,
        user_id: UUID,
        folder_id: str | None = None,
        recursive: bool = False,
        notion_service: SyncNotionService | None = None,
    ):
        return


class MockSyncFilesRepository(SyncFileInterface):
    def __init__(self):
        self.files_store = defaultdict(list)
        self.next_id = 1

    def create_sync_file(self, sync_file_input: SyncFileInput) -> Optional[DBSyncFile]:
        supported = sync_file_input.supported if sync_file_input.supported else True
        new_file = DBSyncFile(
            id=self.next_id,
            path=sync_file_input.path,
            syncs_active_id=sync_file_input.syncs_active_id,
            last_modified=sync_file_input.last_modified,
            brain_id=sync_file_input.brain_id,
            supported=supported,
        )
        self.files_store[sync_file_input.syncs_active_id].append(new_file)
        self.next_id += 1
        return new_file

    def get_sync_files(self, sync_active_id: int) -> List[DBSyncFile]:
        """
        Retrieve sync files from the mock database.

        Args:
            sync_active_id (int): The ID of the active sync.

        Returns:
            List[DBSyncFile]: A list of sync files matching the criteria.
        """
        return self.files_store[sync_active_id]

    def update_sync_file(
        self, sync_file_id: int, sync_file_input: SyncFileUpdateInput
    ) -> None:
        for sync_files in self.files_store.values():
            for file in sync_files:
                if file.id == sync_file_id:
                    update_data = sync_file_input.model_dump(exclude_unset=True)
                    if "last_modified" in update_data:
                        file.last_modified = update_data["last_modified"]
                    if "supported" in update_data:
                        file.supported = update_data["supported"]
                    return

    def update_or_create_sync_file(
        self,
        file: SyncFile,
        sync_active: SyncsActive,
        previous_file: Optional[DBSyncFile],
        supported: bool,
    ) -> Optional[DBSyncFile]:
        if previous_file:
            self.update_sync_file(
                previous_file.id,
                SyncFileUpdateInput(
                    last_modified=file.last_modified,
                    supported=previous_file.supported or supported,
                ),
            )
            return previous_file
        else:
            return self.create_sync_file(
                SyncFileInput(
                    path=file.name,
                    syncs_active_id=sync_active.id,
                    last_modified=file.last_modified,
                    brain_id=str(sync_active.brain_id),
                    supported=supported,
                )
            )

    def delete_sync_file(self, sync_file_id: int) -> None:
        for sync_active_id, sync_files in self.files_store.items():
            self.files_store[sync_active_id] = [
                file for file in sync_files if file.id != sync_file_id
            ]


@pytest.fixture
def sync_file():
    file = SyncFile(
        id=str(uuid4()),
        name="test_file.txt",
        is_folder=False,
        last_modified=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        mime_type=".txt",
        web_view_link="",
        notification_id=uuid4(),  #
    )
    return file


@pytest.fixture
def prev_file():
    file = SyncFile(
        id=str(uuid4()),
        name="test_file.txt",
        is_folder=False,
        last_modified=(datetime.now() - timedelta(hours=1)).strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        mime_type="txt",
        web_view_link="",
        notification_id=uuid4(),  #
    )
    return file


@pytest_asyncio.fixture(scope="function")
async def brain_user_setup(
    session,
) -> Tuple[Brain, User]:
    user_1 = (
        await session.exec(select(User).where(User.email == "admin@quivr.app"))
    ).one()
    # Brain data
    brain_1 = Brain(
        name="test_brain",
        description="this is a test brain",
        brain_type=BrainType.integration,
    )

    session.add(brain_1)
    await session.refresh(user_1)
    await session.commit()
    assert user_1
    assert brain_1.brain_id
    return brain_1, user_1


@pytest_asyncio.fixture(scope="function")
async def setup_syncs_data(
    brain_user_setup,
) -> Tuple[SyncsUser, SyncsActive]:
    brain_1, user_1 = brain_user_setup

    sync_user = SyncsUser(
        id=0,
        user_id=user_1.id,
        name="c8xfz3g566b8xa1ajiesdh",
        provider="mock",
        credentials={},
        state={},
        additional_data={},
    )
    sync_active = SyncsActive(
        id=0,
        name="test",
        syncs_user_id=sync_user.id,
        user_id=sync_user.user_id,
        settings={},
        last_synced=str(datetime.now() - timedelta(hours=5)),
        sync_interval_minutes=1,
        brain_id=brain_1.brain_id,
    )

    return (sync_user, sync_active)


@pytest.fixture
def syncutils(
    sync_file: SyncFile,
    prev_file: SyncFile,
    setup_syncs_data: Tuple[SyncsUser, SyncsActive],
    session,
) -> SyncUtils:
    (sync_user, sync_active) = setup_syncs_data
    assert sync_file.notification_id
    sync_active_service = MockSyncService(sync_active)
    sync_user_service = MockSyncUserService(sync_user)
    sync_files_repo_service = MockSyncFilesRepository()
    knowledge_service = KnowledgeService(KnowledgeRepository(session))
    notification_service = NotificationService(
        repository=MockNotification(
            [sync_file.notification_id, prev_file.notification_id],  # type: ignore
            sync_user.user_id,
            sync_active.brain_id,
        )
    )
    brain_vectors = BrainsVectors()
    sync_cloud = MockSyncCloud()

    sync_util = SyncUtils(
        sync_user_service=sync_user_service,
        sync_active_service=sync_active_service,
        sync_files_repo=sync_files_repo_service,
        sync_cloud=sync_cloud,
        notification_service=notification_service,
        brain_vectors=brain_vectors,
        knowledge_service=knowledge_service,
    )

    return sync_util


@pytest.fixture
def syncutils_notion(
    sync_file: SyncFile,
    prev_file: SyncFile,
    setup_syncs_data: Tuple[SyncsUser, SyncsActive],
    session,
) -> SyncUtils:
    (sync_user, sync_active) = setup_syncs_data
    assert sync_file.notification_id
    sync_active_service = MockSyncService(sync_active)
    sync_user_service = MockSyncUserService(sync_user)
    sync_files_repo_service = MockSyncFilesRepository()
    knowledge_service = KnowledgeService(KnowledgeRepository(session))
    notification_service = NotificationService(
        repository=MockNotification(
            [sync_file.notification_id, prev_file.notification_id],  # type: ignore
            sync_user.user_id,
            sync_active.brain_id,
        )
    )
    brain_vectors = BrainsVectors()
    sync_cloud = MockSyncCloudNotion()
    sync_util = SyncUtils(
        sync_user_service=sync_user_service,
        sync_active_service=sync_active_service,
        sync_files_repo=sync_files_repo_service,
        sync_cloud=sync_cloud,
        notification_service=notification_service,
        brain_vectors=brain_vectors,
        knowledge_service=knowledge_service,
    )

    return sync_util
