import base64
import os
from uuid import UUID

import requests
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from notion_client import Client

from quivr_api.celery_config import celery
from quivr_api.logger import get_logger
from quivr_api.middlewares.auth import AuthBearer, get_current_user
from quivr_api.modules.sync.dto.inputs import SyncsUserInput, SyncUserUpdateInput
from quivr_api.modules.sync.service.sync_service import SyncService, SyncUserService
from quivr_api.modules.user.entity.user_identity import UserIdentity

from .successfull_connection import successfullConnectionPage

NOTION_CLIENT_ID = os.getenv("NOTION_CLIENT_ID")
NOTION_CLIENT_SECRET = os.getenv("NOTION_CLIENT_SECRET")
NOTION_AUTH_URL = os.getenv("NOTION_AUTH_URL")
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
    authorize_url = str(NOTION_AUTH_URL) + f"&state={state}"

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
def oauth2callback_notion(request: Request, background_tasks: BackgroundTasks):
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
    current_user = UUID(state_split[0].split("=")[1]) if state else None
    assert current_user, "Oauth callback user is None"
    logger.debug(
        f"Handling OAuth2 callback for user: {current_user} with state: {state} and state_dict: {state_dict}"
    )
    sync_user_state = sync_user_service.get_sync_user_by_state(state_dict)

    if not sync_user_state or state_dict != sync_user_state.state:
        logger.error(f"Invalid state parameter for {sync_user_state}")
        raise HTTPException(status_code=400, detail="Invalid state parameter")
    else:
        logger.info(
            f"Current user: {current_user}, sync user state: {sync_user_state.state}"
        )

    if sync_user_state.user_id != current_user:
        raise HTTPException(status_code=400, detail="Invalid user")

    try:
        token_url = "https://api.notion.com/v1/oauth/token"
        client_credentials = f"{NOTION_CLIENT_ID}:{NOTION_CLIENT_SECRET}"
        encoded_credentials = base64.b64encode(client_credentials.encode()).decode()

        headers = {
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/json",
        }

        token_data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": BASE_REDIRECT_URI,
        }
        logger.debug(f"Requesting token with data: {token_data}")

        response = requests.post(token_url, headers=headers, json=token_data)
        oauth_result = response.json()
        access_token = oauth_result["access_token"]

        notion = Client(auth=access_token)

        # Get account information
        user_info = notion.users.me()

        owner_info = user_info["bot"]["owner"]["user"]  # type: ignore
        user_email = owner_info["person"]["email"]
        account_id = owner_info["id"]

        result: dict[str, str] = {
            "access_token": access_token,
            "refresh_token": oauth_result.get("refresh_token", ""),
            "account_id": account_id,
            "expires_in": oauth_result.get("expires_in", ""),
        }

        sync_user_input = SyncUserUpdateInput(
            credentials=result,
            state={},
            email=user_email,
        )
        sync_user_service.update_sync_user(current_user, state_dict, sync_user_input)
        logger.info(f"Notion sync created successfully for user: {current_user}")
        # launch celery task to sync notion data
        celery.send_task(
            "fetch_and_store_notion_files_task",
            kwargs={"access_token": access_token, "user_id": current_user},
        )
        return HTMLResponse(successfullConnectionPage)

    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=400, detail="Invalid user")
