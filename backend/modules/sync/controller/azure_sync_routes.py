import os

from fastapi import APIRouter, Depends, HTTPException, Request
from logger import get_logger
from middlewares.auth import AuthBearer, get_current_user
from modules.sync.dto.inputs import SyncsUserInput, SyncUserUpdateInput
from modules.sync.service.sync_service import SyncService, SyncUserService
from modules.user.entity.user_identity import UserIdentity
from msal import PublicClientApplication

# Initialize logger
logger = get_logger(__name__)

# Initialize sync service
sync_service = SyncService()
sync_user_service = SyncUserService()

# Initialize API router
azure_sync_router = APIRouter()

# Constants
CLIENT_ID = os.getenv("SHAREPOINT_CLIENT_ID")
AUTHORITY = "https://login.microsoftonline.com/common"
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:5050")
REDIRECT_URI = f"{BACKEND_URL}/sync/azure/oauth2callback"
SCOPE = [
    "https://graph.microsoft.com/Files.Read",
    "https://graph.microsoft.com/User.Read",
    "https://graph.microsoft.com/Sites.Read.All",
]


@azure_sync_router.get(
    "/sync/azure/authorize",
    dependencies=[Depends(AuthBearer())],
    tags=["Sync"],
)
def authorize_azure(
    request: Request, name: str, current_user: UserIdentity = Depends(get_current_user)
):
    """
    Authorize Azure sync for the current user.

    Args:
        request (Request): The request object.
        current_user (UserIdentity): The current authenticated user.

    Returns:
        dict: A dictionary containing the authorization URL.
    """
    client = PublicClientApplication(CLIENT_ID, authority=AUTHORITY)
    logger.debug(f"Authorizing Azure sync for user: {current_user.id}")
    state = f"user_id={current_user.id}"
    authorization_url = client.get_authorization_request_url(
        scopes=SCOPE, redirect_uri=REDIRECT_URI, state=state
    )

    sync_user_input = SyncsUserInput(
        user_id=str(current_user.id),
        name=name,
        provider="Azure",
        credentials={},
        state={"state": state},
    )
    sync_user_service.create_sync_user(sync_user_input)
    return {"authorization_url": authorization_url}


@azure_sync_router.get("/sync/azure/oauth2callback", tags=["Sync"])
def oauth2callback_azure(request: Request):
    """
    Handle OAuth2 callback from Azure.

    Args:
        request (Request): The request object.

    Returns:
        dict: A dictionary containing a success message.
    """
    client = PublicClientApplication(CLIENT_ID, authority=AUTHORITY)
    state = request.query_params.get("state")
    state_dict = {"state": state}
    current_user = state.split("=")[1]  # Extract user_id from state
    logger.debug(
        f"Handling OAuth2 callback for user: {current_user} with state: {state}"
    )
    sync_user_state = sync_user_service.get_sync_user_by_state(state_dict)
    logger.info(f"Retrieved sync user state: {sync_user_state}")

    if state_dict != sync_user_state["state"]:
        logger.error("Invalid state parameter")
        raise HTTPException(status_code=400, detail="Invalid state parameter")
    if sync_user_state.get("user_id") != current_user:
        logger.error("Invalid user")
        raise HTTPException(status_code=400, detail="Invalid user")

    result = client.acquire_token_by_authorization_code(
        request.query_params.get("code"), scopes=SCOPE, redirect_uri=REDIRECT_URI
    )
    if "access_token" not in result:
        logger.error("Failed to acquire token")
        raise HTTPException(status_code=400, detail="Failed to acquire token")

    creds = result
    logger.info(f"Fetched OAuth2 token for user: {current_user}")

    sync_user_input = SyncUserUpdateInput(
        credentials=creds,
        state={},
    )
    sync_user_service.update_sync_user(current_user, state_dict, sync_user_input)
    logger.info(f"Azure sync created successfully for user: {current_user}")
    return {"message": "Azure sync created successfully"}
