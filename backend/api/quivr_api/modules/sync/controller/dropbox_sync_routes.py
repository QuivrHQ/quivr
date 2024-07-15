import os

from dropbox import Dropbox, DropboxOAuth2Flow
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from quivr_api.logger import get_logger
from quivr_api.middlewares.auth import AuthBearer, get_current_user
from quivr_api.modules.sync.dto.inputs import SyncsUserInput
from quivr_api.modules.sync.service.sync_service import SyncService, SyncUserService
from quivr_api.modules.user.entity.user_identity import UserIdentity

from .successfull_connection import successfullConnectionPage

DROPBOX_APP_KEY = os.getenv("DROPBOX_APP_KEY")
DROPBOX_APP_SECRET = os.getenv("DROPBOX_APP_SECRET")
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:5050")
BASE_REDIRECT_URI = f"{BACKEND_URL}/sync/dropbox/oauth2callback"
SCOPE = ["files.metadata.read"]

# Initialize sync service
sync_service = SyncService()
sync_user_service = SyncUserService()

logger = get_logger(__name__)

# Initialize API router
dropbox_sync_router = APIRouter()


@dropbox_sync_router.post(
    "/sync/dropbox/authorize",
    dependencies=[Depends(AuthBearer())],
    tags=["Sync"],
)
def authorize_dropbox(
    request: Request, name: str, current_user: UserIdentity = Depends(get_current_user)
):
    """
    Authorize DropBox sync for the current user.

    Args:
        request (Request): The request object.
        current_user (UserIdentity): The current authenticated user.

    Returns:
        dict: A dictionary containing the authorization URL.
    """
    logger.debug(f"Authorizing Drop Box sync for user: {current_user.id}")
    auth_flow = DropboxOAuth2Flow(
        DROPBOX_APP_KEY,
        redirect_uri=BASE_REDIRECT_URI,
        session=request.session,
        csrf_token_session_key="dropbox-auth-csrf-token",
        consumer_secret=DROPBOX_APP_SECRET,
        token_access_type="offline",
        scope=SCOPE,
    )
    state: str = f"user_id={current_user.id}, name={name}"
    authorize_url = auth_flow.start(state)

    logger.info(
        f"Generated authorization URL: {authorize_url} for user: {current_user.id}"
    )
    sync_user_input = SyncsUserInput(
        name=name,
        user_id=str(current_user.id),
        provider="DropBox",
        credentials={},
        state={"state": state},
    )
    request.session["csrf-token"] = auth_flow.csrf_token_session_key
    sync_user_service.create_sync_user(sync_user_input)
    return {"authorization_url": authorize_url}


# {'state': 'dNzjXyh7CuAFyrBhKNG-UQ==|user_id=39418e3b-0258-4452-af60-7acfcc1263ff, name=chloe'}
# {'state': 'user_id=39418e3b-0258-4452-af60-7acfcc1263ff, name=chloe'}
@dropbox_sync_router.get("/sync/dropbox/oauth2callback", tags=["Sync"])
def oauth2callback_dropbox(request: Request):
    """
    Handle OAuth2 callback from DropBox.

    Args:
        request (Request): The request object.

    Returns:
        dict: A dictionary containing a success message.
    """
    state = request.query_params.get("state")
    logger.info(f"------- State: {state}")
    state = state.split("|")[1] if "|" in state else state  # type: ignore
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
        logger.error("Invalid user")
        logger.info(f"Invalid user: {current_user}")
        raise HTTPException(status_code=400, detail="Invalid user")

    redirect_uri = f"{BASE_REDIRECT_URI}"
    auth_flow = DropboxOAuth2Flow(
        DROPBOX_APP_KEY,
        redirect_uri=BASE_REDIRECT_URI,
        session=request.session,
        csrf_token_session_key="dropbox-auth-csrf-token",
        consumer_secret=DROPBOX_APP_SECRET,
        token_access_type="offline",
        scope=SCOPE,
    )
    try:
        logger.debug(f"QUERY PARAM : {request.query_params.get('code')}")
        oauth_result = auth_flow.finish(request.query_params)
        logger.debug(f"RESULT : {oauth_result}")

        access_token = oauth_result.access_token

        dbx = Dropbox(oauth2_access_token=access_token)

        # Get account information
        account_info = dbx.users_get_current_account()
        email = account_info.email  # type: ignore
        account_id = account_info.account_id  # type: ignore

        logger.info(f"Retrieved email for user: {current_user} - {email}")
        logger.info(f"OAuth Result: {oauth_result}")

        # sync_user_input = SyncUserUpdateInput(
        # credentials=json.loads(oauth_result.to_json()),
        # state={},
        # email=email,
        # )
        # sync_user_service.update_sync_user(str(current_user), state_dict, sync_user_input)
        # logger.info(f"Google Drive sync created successfully for user: {current_user}")
        return HTMLResponse(successfullConnectionPage)
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=400, detail="Invalid user")
