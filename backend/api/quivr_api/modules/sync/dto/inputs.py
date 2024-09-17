from uuid import UUID

from pydantic import BaseModel


class SyncCreateInput(BaseModel):
    """
    Input model for creating a new sync user.

    Attributes:
        user_id (str): The unique identifier for the user.
        name (str): The name of the user.
        provider (str): The provider of the sync service (e.g., Google, Azure).
        credentials (dict): The credentials required for the sync service.
        state (dict): The state information for the sync user.
    """

    user_id: UUID
    name: str
    provider: str
    credentials: dict
    state: dict
    additional_data: dict = {}


class SyncUpdateInput(BaseModel):
    """
    Input model for updating an existing sync user.

    Attributes:
        credentials (dict): The updated credentials for the sync service.
        state (dict): The updated state information for the sync user.
    """

    credentials: dict
    state: dict
    email: str
