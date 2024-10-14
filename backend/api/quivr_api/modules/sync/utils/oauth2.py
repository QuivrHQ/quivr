from uuid import UUID

from fastapi import HTTPException, status
from pydantic import BaseModel

from quivr_api.logger import get_logger

logger = get_logger(__name__)


class Oauth2BaseState(BaseModel):
    name: str
    user_id: UUID


class Oauth2State(Oauth2BaseState):
    sync_id: int


def parse_oauth2_state(state_str: str | None) -> Oauth2State:
    if not state_str:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid state parameter"
        )

    state = Oauth2State.model_validate_json(state_str)
    if state.sync_id is None:
        raise HTTPException(
            status_code=400, detail="Invalid state parameter. Unknown sync"
        )
    return state
