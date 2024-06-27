import json
import os

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from quivr_api.logger import get_logger
from quivr_api.middlewares.auth import AuthBearer, get_current_user
from quivr_api.modules.sync.dto.inputs import SyncsUserInput, SyncUserUpdateInput
from quivr_api.modules.sync.service.sync_service import SyncService, SyncUserService
from quivr_api.modules.user.entity.user_identity import UserIdentity

from .successfull_connection import successfullConnectionPage

# Set environment variable for OAuthlib
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

# Initialize logger
logger = get_logger(__name__)

# Initialize sync service
sync_service = SyncService()
sync_user_service = SyncUserService()

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
def authorize_google(
    request: Request, name: str, current_user: UserIdentity = Depends(get_current_user)
):
    """
    Authorize Google Drive sync for the current user.

    Args:
        request (Request): The request object.
        current_user (UserIdentity): The current authenticated user.

    Returns:
        dict: A dictionary containing the authorization URL.
    """
    logger.debug(f"Authorizing Google Drive sync for user: {current_user.id}")
    redirect_uri = BASE_REDIRECT_URI
    flow = Flow.from_client_config(
        CLIENT_SECRETS_FILE_CONTENT,
        scopes=SCOPES,
        redirect_uri=redirect_uri,
    )
    state = f"user_id={current_user.id}, name={name}"
    authorization_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        state=state,
        prompt="consent",
    )
    logger.info(
        f"Generated authorization URL: {authorization_url} for user: {current_user.id}"
    )
    sync_user_input = SyncsUserInput(
        name=name,
        user_id=str(current_user.id),
        provider="Google",
        credentials={},
        state={"state": state},
    )
    sync_user_service.create_sync_user(sync_user_input)
    return {"authorization_url": authorization_url}


@google_sync_router.get("/sync/google/oauth2callback", tags=["Sync"])
def oauth2callback_google(request: Request):
    """
    Handle OAuth2 callback from Google.

    Args:
        request (Request): The request object.

    Returns:
        dict: A dictionary containing a success message.
    """
    state = request.query_params.get("state")
    state_dict = {"state": state}
    logger.info(f"State: {state}")
    state_split = state.split(",")
    current_user = state_split[0].split("=")[1] if state else None
    name = state_split[1].split("=")[1] if state else None
    logger.debug(
        f"Handling OAuth2 callback for user: {current_user} with state: {state}"
    )
    sync_user_state = sync_user_service.get_sync_user_by_state(state_dict)
    logger.info(f"Retrieved sync user state: {sync_user_state}")

    if not sync_user_state or state_dict != sync_user_state.get("state"):
        logger.error("Invalid state parameter")
        raise HTTPException(status_code=400, detail="Invalid state parameter")
    if sync_user_state.get("user_id") != current_user:
        logger.error("Invalid user")
        logger.info(f"Invalid user: {current_user}")
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
    logger.info(f"Fetched OAuth2 token for user: {current_user}")

    # Use the credentials to get the user's email
    service = build("oauth2", "v2", credentials=creds)
    user_info = service.userinfo().get().execute()
    user_email = user_info.get("email")
    logger.info(f"Retrieved email for user: {current_user} - {user_email}")

    sync_user_input = SyncUserUpdateInput(
        credentials=json.loads(creds.to_json()),
        state={},
        email=user_email,
    )
    sync_user_service.update_sync_user(current_user, state_dict, sync_user_input)
    logger.info(f"Google Drive sync created successfully for user: {current_user}")
    return HTMLResponse(successfullConnectionPage)
