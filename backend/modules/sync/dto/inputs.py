from typing import List, Optional

from pydantic import BaseModel


class SyncsUserInput(BaseModel):
    """
    Input model for creating a new sync user.

    Attributes:
        user_id (str): The unique identifier for the user.
        name (str): The name of the user.
        provider (str): The provider of the sync service (e.g., Google, Azure).
        credentials (dict): The credentials required for the sync service.
        state (dict): The state information for the sync user.
    """

    user_id: str
    name: str
    provider: str
    credentials: dict
    state: dict


class SyncUserUpdateInput(BaseModel):
    """
    Input model for updating an existing sync user.

    Attributes:
        credentials (dict): The updated credentials for the sync service.
        state (dict): The updated state information for the sync user.
    """

    credentials: dict
    state: dict
    email: str


class SyncActiveSettings(BaseModel):
    """
    Sync active settings.

    Attributes:
        folders (List[str] | None): A list of folder paths to be synced, or None if not applicable.
        files (List[str] | None): A list of file paths to be synced, or None if not applicable.
    """

    folders: Optional[List[str]] = None
    files: Optional[List[str]] = None


class SyncsActiveInput(BaseModel):
    """
    Input model for creating a new active sync.

    Attributes:
        name (str): The name of the sync.
        syncs_user_id (int): The ID of the sync user associated with this sync.
        settings (SyncActiveSettings): The settings for the active sync.
    """

    name: str
    syncs_user_id: int
    settings: SyncActiveSettings
    brain_id: str


class SyncsActiveUpdateInput(BaseModel):
    """
    Input model for updating an existing active sync.

    Attributes:
        name (str): The updated name of the sync.
        sync_interval_minutes (int): The updated sync interval in minutes.
        settings (dict): The updated settings for the active sync.
    """

    name: Optional[str] = None
    settings: Optional[SyncActiveSettings] = None
    last_synced: Optional[str] = None
    force_sync: Optional[bool] = False


class SyncFileInput(BaseModel):
    """
    Input model for creating a new sync file.

    Attributes:
        path (str): The path of the file.
        syncs_active_id (int): The ID of the active sync associated with this file.
    """

    path: str
    syncs_active_id: int
    last_modified: str
    brain_id: str
    supported: Optional[bool] = True


class SyncFileUpdateInput(BaseModel):
    """
    Input model for updating an existing sync file.

    Attributes:
        last_modified (datetime.datetime): The updated last modified date and time.
    """

    last_modified: Optional[str] = None
    supported: Optional[bool] = None
