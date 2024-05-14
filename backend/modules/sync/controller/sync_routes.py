import json
import os
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request
from google_auth_oauthlib.flow import Flow
from logger import get_logger
from middlewares.auth import AuthBearer, get_current_user
from modules.sync.dto import SyncsDescription
from modules.sync.dto.inputs import SyncsUserInput, SyncUserUpdateInput
from modules.sync.dto.outputs import AuthMethodEnum
from modules.sync.service.sync_service import SyncService
from modules.user.entity.user_identity import UserIdentity

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

logger = get_logger(__name__)

sync_service = SyncService()

sync_router = APIRouter()

google_sync = SyncsDescription(
    name="Google",
    description="Sync your Google Drive with Quivr",
    auth_method=AuthMethodEnum.URI_WITH_CALLBACK,
)


@sync_router.get(
    "/sync/all",
    response_model=List[SyncsDescription],
    dependencies=[Depends(AuthBearer())],
    tags=["Sync"],
)
async def get_syncs(current_user: UserIdentity = Depends(get_current_user)):

    return [google_sync]


@sync_router.get(
    "/sync",
    dependencies=[Depends(AuthBearer())],
    tags=["Sync"],
)
async def get_user_syncs(current_user: UserIdentity = Depends(get_current_user)):

    return sync_service.get_syncs_user(str(current_user.id))


CLIENT_SECRETS_FILE = "modules/sync/controller/credentials.json"
SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly"]
REDIRECT_URI = "http://localhost:5050/sync/google/oauth2callback"


@sync_router.get(
    "/sync/google/authorize",
    dependencies=[Depends(AuthBearer())],
    tags=["Sync"],
)
def authorize_google(
    request: Request, current_user: UserIdentity = Depends(get_current_user)
):
    # Add to the redirect URI the user_id to be able to identify the user when the callback is called
    REDIRECT_URI = (
        f"http://localhost:5050/sync/google/oauth2callback?user_id={current_user.id}"
    )
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES, redirect_uri=REDIRECT_URI
    )
    authorization_url, state = flow.authorization_url(
        access_type="offline", include_granted_scopes="true"
    )
    sync_user_input = SyncsUserInput(
        user_id=str(current_user.id),
        sync_name="Google",
        credentials={},
        state={"state": state},
    )
    sync_service.create_sync_user(sync_user_input)
    return {"authorization_url": authorization_url}


@sync_router.get("/sync/google/oauth2callback")
def oauth2callback_google(request: Request):
    state = request.query_params.get("state")
    state_dict = {"state": state}
    current_user = request.query_params.get("user_id")
    sync_user_state = sync_service.get_sync_user_by_state(state_dict)
    logger.info(sync_user_state)
    if state_dict != sync_user_state["state"]:
        raise HTTPException(status_code=400, detail="Invalid state parameter")

    if sync_user_state.get("user_id") != current_user:
        raise HTTPException(status_code=400, detail="Invalid user")

    REDIRECT_URI = (
        f"http://localhost:5050/sync/google/oauth2callback?user_id={current_user}"
    )
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES, state=state, redirect_uri=REDIRECT_URI
    )
    flow.fetch_token(authorization_response=str(request.url))
    creds = flow.credentials

    sync_user_input = SyncUserUpdateInput(
        credentials=json.loads(creds.to_json()),
        state={},
    )
    sync_service.update_sync_user(current_user, state_dict, sync_user_input)
    return {"message": "Google Drive sync created successfully"}
