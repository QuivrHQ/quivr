import os

import requests
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from msal import ConfidentialClientApplication

from quivr_api.logger import get_logger
from quivr_api.middlewares.auth import AuthBearer, get_current_user
from quivr_api.modules.dependencies import get_service
from quivr_api.modules.sync.dto.inputs import SyncCreateInput, SyncUpdateInput
from quivr_api.modules.sync.service.sync_service import SyncsService
from quivr_api.modules.sync.utils.oauth2 import Oauth2State
from quivr_api.modules.sync.utils.sync_exceptions import SyncNotFoundException
from quivr_api.modules.user.entity.user_identity import UserIdentity

from .successfull_connection import successfullConnectionPage

# Initialize logger
logger = get_logger(__name__)


syncs_service_dep = get_service(SyncsService)

# Initialize API router
azure_sync_router = APIRouter()

# Constants
CLIENT_ID = os.getenv("SHAREPOINT_CLIENT_ID")
CLIENT_SECRET = os.getenv("SHAREPOINT_CLIENT_SECRET")
AUTHORITY = "https://login.microsoftonline.com/common"
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:5050")
REDIRECT_URI = f"{BACKEND_URL}/sync/azure/oauth2callback"
SCOPE = [
    "https://graph.microsoft.com/Files.Read",
    "https://graph.microsoft.com/User.Read",
    "https://graph.microsoft.com/Sites.Read.All",
]


@azure_sync_router.post(
    "/sync/azure/authorize",
    dependencies=[Depends(AuthBearer())],
    tags=["Sync"],
)
async def authorize_azure(
    request: Request,
    name: str,
    syncs_service: SyncsService = Depends(syncs_service_dep),
    current_user: UserIdentity = Depends(get_current_user),
):
    """
    Authorize Azure sync for the current user.

    Args:
        request (Request): The request object.
        current_user (UserIdentity): The current authenticated user.

    Returns:
        dict: A dictionary containing the authorization URL.
    """
    client = ConfidentialClientApplication(
        CLIENT_ID, client_credential=CLIENT_SECRET, authority=AUTHORITY
    )
    logger.debug(f"Authorizing Azure sync for user: {current_user.id}")
    state_struct = Oauth2State(name=name, user_id=current_user.id)
    state = state_struct.model_dump_json()

    sync_user_input = SyncCreateInput(
        user_id=current_user.id,
        name=name,
        provider="Azure",
        credentials={},
        state={"state": state},
    )
    sync = await syncs_service.create_sync_user(sync_user_input)
    state_struct.sync_id = sync.id
    state = state_struct.model_dump_json()

    flow = client.initiate_auth_code_flow(
        scopes=SCOPE, redirect_uri=REDIRECT_URI, state=state, prompt="select_account"
    )

    sync = await syncs_service.update_sync(
        sync_id=sync.id,
        sync_user_input=SyncUpdateInput(
            **{**sync.model_dump(), "additional_data": {"flow": flow}}
        ),
    )
    return {"authorization_url": flow["auth_uri"]}


@azure_sync_router.get("/sync/azure/oauth2callback", tags=["Sync"])
async def oauth2callback_azure(
    request: Request,
    syncs_service: SyncsService = Depends(syncs_service_dep),
):
    """
    Handle OAuth2 callback from Azure.

    Args:
        request (Request): The request object.

    Returns:
        dict: A dictionary containing a success message.
    """
    client = ConfidentialClientApplication(
        CLIENT_ID, client_credential=CLIENT_SECRET, authority=AUTHORITY
    )
    state = request.query_params.get("state")

    if not state:
        raise HTTPException(status_code=400, detail="Invalid state parameter")

    state = Oauth2State.model_validate_json(state)

    if state.sync_id is None:
        raise HTTPException(
            status_code=400, detail="Invalid state parameter. Unknown sync"
        )

    logger.debug(
        f"Handling OAuth2 callback for user: {state.user_id} with state: {state}"
    )

    try:
        sync = await syncs_service.get_sync_by_id(state.sync_id)
    except SyncNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"{e.message}"
        )
    if (
        not sync
        or not sync.state
        or state.model_dump(exclude={"sync_id"}) != sync.state["state"]
    ):
        logger.error("Invalid state parameter")
        raise HTTPException(status_code=400, detail="Invalid state parameter")

    if sync.user_id != state.user_id:
        raise HTTPException(status_code=400, detail="Invalid user")

    if sync.additional_data is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid sync data"
        )

    result = client.acquire_token_by_auth_code_flow(
        sync.additional_data["flow"], dict(request.query_params)
    )
    if "access_token" not in result:
        logger.error(f"Failed to acquire token: {result}")
        raise HTTPException(
            status_code=400,
            detail=f"Failed to acquire token: {result}",
        )

    access_token = result["access_token"]

    creds = result
    logger.info(f"Fetched OAuth2 token for user: {state.user_id}")

    # Fetch user email from Microsoft Graph API
    graph_url = "https://graph.microsoft.com/v1.0/me"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(graph_url, headers=headers)
    if response.status_code != 200:
        logger.error("Failed to fetch user profile from Microsoft Graph API")
        raise HTTPException(status_code=400, detail="Failed to fetch user profile")

    user_info = response.json()
    user_email = user_info.get("mail") or user_info.get("userPrincipalName")
    logger.info(f"Retrieved email for user: {state.user_id} - {user_email}")

    sync_user_input = SyncUpdateInput(credentials=result, state={}, email=user_email)

    await syncs_service.update_sync(state.sync_id, sync_user_input)
    logger.info(f"Azure sync created successfully for user: {state.user_id}")
    return HTMLResponse(successfullConnectionPage)
