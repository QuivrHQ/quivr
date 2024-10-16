import os

import requests
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from msal import ConfidentialClientApplication

from quivr_api.logger import get_logger
from quivr_api.middlewares.auth import AuthBearer, get_current_user
from quivr_api.modules.dependencies import get_service
from quivr_api.modules.sync.dto.inputs import SyncStatus, SyncUpdateInput
from quivr_api.modules.sync.dto.outputs import SyncProvider
from quivr_api.modules.sync.service.sync_service import SyncsService
from quivr_api.modules.sync.utils.oauth2 import parse_oauth2_state
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
    state = await syncs_service.create_oauth2_state(
        provider=SyncProvider.AZURE, name=name, user_id=current_user.id
    )
    flow = client.initiate_auth_code_flow(
        scopes=SCOPE,
        redirect_uri=REDIRECT_URI,
        state=state.model_dump_json(),
        prompt="select_account",
    )
    # Azure needs additional data
    await syncs_service.update_sync(
        sync_id=state.sync_id,
        sync_user_input=SyncUpdateInput(
            additional_data={"flow": flow}, status=SyncStatus.SYNCED
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
    state_str = request.query_params.get("state")
    state = parse_oauth2_state(state_str)
    logger.debug(
        f"Handling OAuth2 callback for user: {state.user_id} with state: {state}"
    )
    sync = await syncs_service.get_from_oauth2_state(state)
    if sync.additional_data is None:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

    flow_data = client.acquire_token_by_auth_code_flow(
        sync.additional_data["flow"], dict(request.query_params)
    )

    if "access_token" not in flow_data:
        logger.error(f"Failed to acquire token: {flow_data}")
        raise HTTPException(
            status_code=400,
            detail=f"Failed to acquire token: {flow_data}",
        )

    access_token = flow_data["access_token"]
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

    sync_user_input = SyncUpdateInput(
        credentials=flow_data, state={}, email=user_email, status=SyncStatus.SYNCED
    )
    await syncs_service.update_sync(state.sync_id, sync_user_input)
    logger.info(f"Azure sync created successfully for user: {state.user_id}")
    return HTMLResponse(successfullConnectionPage)
