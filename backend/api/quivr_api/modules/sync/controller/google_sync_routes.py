import json
import os

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

from quivr_api.logger import get_logger
from quivr_api.middlewares.auth import AuthBearer, get_current_user
from quivr_api.modules.dependencies import get_service
from quivr_api.modules.sync.dto.inputs import SyncCreateInput, SyncUpdateInput
from quivr_api.modules.sync.service.sync_service import SyncsService
from quivr_api.modules.sync.utils.oauth2 import Oauth2State
from quivr_api.modules.sync.utils.sync_exceptions import SyncNotFoundException
from quivr_api.modules.user.entity.user_identity import UserIdentity

from .successfull_connection import successfullConnectionPage

# Set environment variable for OAuthlib
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

# Initialize logger
logger = get_logger(__name__)

# Initialize sync service
syncs_service_dep = get_service(SyncsService)

# Initialize API router
google_sync_router = APIRouter()

# Constants
SCOPES = [
    "https://www.googleapis.com/auth/drive.metadata.readonly",
    "https://www.googleapis.com/auth/drive.readonly",
    "https://www.googleapis.com/auth/userinfo.email",
    "openid",
]
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:5050")
BASE_REDIRECT_URI = f"{BACKEND_URL}/sync/google/oauth2callback"

# Create credentials content from environment variables
CLIENT_SECRETS_FILE_CONTENT = {
    "installed": {
        "client_id": os.getenv("GOOGLE_CLIENT_ID"),
        "project_id": os.getenv("GOOGLE_PROJECT_ID"),
        "auth_uri": os.getenv("GOOGLE_AUTH_URI"),
        "token_uri": os.getenv("GOOGLE_TOKEN_URI"),
        "auth_provider_x509_cert_url": os.getenv("GOOGLE_AUTH_PROVIDER_CERT_URL"),
        "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
        "redirect_uris": os.getenv("GOOGLE_REDIRECT_URI", "http://localhost").split(
            ","
        ),
        "javascript_origins": os.getenv(
            "GOOGLE_JAVASCRIPT_ORIGINS", "http://localhost"
        ).split(","),
    }
}


@google_sync_router.post(
    "/sync/google/authorize",
    dependencies=[Depends(AuthBearer())],
    tags=["Sync"],
)
async def authorize_google(
    request: Request,
    name: str,
    current_user: UserIdentity = Depends(get_current_user),
    syncs_service: SyncsService = Depends(syncs_service_dep),
):
    """
    Authorize Google Drive sync for the current user.

    Args:
        request (Request): The request object.
        current_user (UserIdentity): The current authenticated user.

    Returns:
        dict: A dictionary containing the authorization URL.
    """
    logger.debug(
        f"Authorizing Google Drive sync for user: {current_user.id}, name : {name}"
    )
    redirect_uri = BASE_REDIRECT_URI
    flow = Flow.from_client_config(
        CLIENT_SECRETS_FILE_CONTENT,
        scopes=SCOPES,
        redirect_uri=redirect_uri,
    )
    state_struct = Oauth2State(name=name, user_id=current_user.id)
    state = state_struct.model_dump_json()
    sync_user_input = SyncCreateInput(
        name=name,
        user_id=current_user.id,
        provider="Google",
        credentials={},
        state={"state": state},
        additional_data={},
    )
    sync = await syncs_service.create_sync_user(sync_user_input)
    state_struct.sync_id = sync.id
    state = state_struct.model_dump_json()
    authorization_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        state=state,
        prompt="consent",
    )
    logger.info(
        f"Generated authorization URL: {authorization_url} for user: {current_user.id}"
    )
    return {"authorization_url": authorization_url}


@google_sync_router.get("/sync/google/oauth2callback", tags=["Sync"])
async def oauth2callback_google(
    request: Request,
    syncs_service: SyncsService = Depends(syncs_service_dep),
):
    """
    Handle OAuth2 callback from Google.

    Args:
        request (Request): The request object.

    Returns:
        dict: A dictionary containing a success message.
    """
    state = request.query_params.get("state")
    logger.debug(f"request state: {state}")
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

    redirect_uri = f"{BASE_REDIRECT_URI}"
    flow = Flow.from_client_config(
        CLIENT_SECRETS_FILE_CONTENT,
        scopes=SCOPES,
        state=state,
        redirect_uri=redirect_uri,
    )
    flow.fetch_token(authorization_response=str(request.url))
    creds = flow.credentials
    logger.info(f"Fetched OAuth2 token for user: {state.user_id}")

    # Use the credentials to get the user's email
    service = build("oauth2", "v2", credentials=creds)
    user_info = service.userinfo().get().execute()
    user_email = user_info.get("email")
    logger.info(f"Retrieved email for user: {state.user_id} - {user_email}")

    sync_user_input = SyncUpdateInput(
        credentials=json.loads(creds.to_json()),
        state={},
        email=user_email,
    )
    sync = await syncs_service.update_sync(state.sync_id, sync_user_input)
    logger.info(f"Google Drive sync created successfully for user: {state.user_id}")
    return HTMLResponse(successfullConnectionPage)
