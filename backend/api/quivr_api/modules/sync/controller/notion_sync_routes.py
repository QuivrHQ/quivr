import os

import requests
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from notion_client import Client
from quivr_api.logger import get_logger
from quivr_api.middlewares.auth import AuthBearer, get_current_user
from quivr_api.modules.sync.dto.inputs import SyncsUserInput, SyncUserUpdateInput
from quivr_api.modules.sync.service.sync_service import SyncService, SyncUserService
from quivr_api.modules.user.entity.user_identity import UserIdentity

from .successfull_connection import successfullConnectionPage

NOTION_CLIENT_ID = os.getenv("NOTION_CLIENT_ID")
NOTION_CLIENT_SECRET = os.getenv("NOTION_CLIENT_SECRET")
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:5050")
BASE_REDIRECT_URI = f"{BACKEND_URL}/sync/notion/oauth2callback"
SCOPE = "users.read,databases.read,databases.write,blocks.read,blocks.write"

# Initialize sync service
sync_service = SyncService()
sync_user_service = SyncUserService()

logger = get_logger(__name__)

# Initialize API router
notion_sync_router = APIRouter()


@notion_sync_router.post(
    "/sync/notion/authorize",
    dependencies=[Depends(AuthBearer())],
    tags=["Sync"],
)
def authorize_notion(
    request: Request, name: str, current_user: UserIdentity = Depends(get_current_user)
):
    """
    Authorize Notion sync for the current user.

    Args:
        request (Request): The request object.
        current_user (UserIdentity): The current authenticated user.

    Returns:
        dict: A dictionary containing the authorization URL.
    """
    logger.debug(f"Authorizing Notion sync for user: {current_user.id}, name : {name}")
    state: str = f"user_id={current_user.id}, name={name}"
    authorize_url = (
        f"https://api.notion.com/v1/oauth/authorize?client_id={NOTION_CLIENT_ID}"
        f"&redirect_uri={BASE_REDIRECT_URI}&response_type=code&owner=user&scope={SCOPE}&state={state}"
    )

    logger.info(
        f"Generated authorization URL: {authorize_url} for user: {current_user.id}"
    )
    sync_user_input = SyncsUserInput(
        name=name,
        user_id=str(current_user.id),
        provider="Notion",
        credentials={},
        state={"state": state},
    )
    sync_user_service.create_sync_user(sync_user_input)
    return {"authorization_url": authorize_url}


@notion_sync_router.get("/sync/notion/oauth2callback", tags=["Sync"])
def oauth2callback_notion(request: Request):
    """
    Handle OAuth2 callback from Notion.

    Args:
        request (Request): The request object.

    Returns:
        dict: A dictionary containing a success message.
    """
    code = request.query_params.get("code")
    state = request.query_params.get("state")
    if not state:
        raise HTTPException(status_code=400, detail="Invalid state parameter")

    state_dict = {"state": state}
    state_split = state.split(",")  # type: ignore
    current_user = state_split[0].split("=")[1] if state else None
    name = state_split[1].split("=")[1] if state else None
    logger.debug(
        f"Handling OAuth2 callback for user: {current_user} with state: {state} and state_dict: {state_dict}"
    )
    sync_user_state = sync_user_service.get_sync_user_by_state(state_dict)

    if not sync_user_state or state_dict != sync_user_state.get("state"):
        logger.error("Invalid state parameter")
        raise HTTPException(status_code=400, detail="Invalid state parameter")
    else:
        logger.info(
            f"CURRENT USER: {current_user}, SYNC USER STATE USER: {sync_user_state.get('user_id')}"
        )

    if sync_user_state.get("user_id") != current_user:
        raise HTTPException(status_code=400, detail="Invalid user")

    try:
        response = requests.post(
            "https://api.notion.com/v1/oauth/token",
            data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": BASE_REDIRECT_URI,
                "client_id": NOTION_CLIENT_ID,
                "client_secret": NOTION_CLIENT_SECRET,
            },
        )
        response.raise_for_status()
        oauth_result = response.json()
        access_token = oauth_result["access_token"]

        notion = Client(auth=access_token)

        # Get account information
        user_info = notion.users.me()
        user_email = user_info["email"]
        account_id = user_info["id"]

        result: dict[str, str] = {
            "access_token": oauth_result["access_token"],
            "refresh_token": oauth_result.get("refresh_token", ""),
            "account_id": account_id,
            "expires_in": oauth_result.get("expires_in", ""),
        }

        sync_user_input = SyncUserUpdateInput(
            credentials=result,
            state={},
            email=user_email,
        )
        sync_user_service.update_sync_user(
            str(current_user), state_dict, sync_user_input
        )
        logger.info(f"Notion sync created successfully for user: {current_user}")
        return HTMLResponse(successfullConnectionPage)
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=400, detail="Invalid user")
