
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
import random

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from quivr_api.logger import get_logger
from quivr_api.middlewares.auth import AuthBearer, get_current_user
from quivr_api.modules.sync.dto.inputs import (
    SyncsUserInput,
    SyncsUserStatus,
    SyncUserUpdateInput,
)
from quivr_api.modules.sync.service.sync_service import SyncService, SyncUserService
from quivr_api.modules.user.entity.user_identity import UserIdentity

from quivr_api.logger import get_logger
from quivr_api.middlewares.auth import AuthBearer, get_current_user
from quivr_api.modules.sync.dto.inputs import (
    SyncsUserInput,
    SyncsUserStatus,
    SyncUserUpdateInput,
)
from quivr_api.modules.sync.service.sync_service import SyncService, SyncUserService
from quivr_api.modules.user.entity.user_identity import UserIdentity
from fastapi import Form

from .successfull_connection import successfullConnectionPage

# Initialize logger
logger = get_logger(__name__)

# Initialize sync service
sync_service = SyncService()
sync_user_service = SyncUserService()

# Initialize API router
zendesk_sync_router = APIRouter()

    # 


@zendesk_sync_router.post(
    "/sync/zendesk/authorize",
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

    state = random.randint(100000, 999999)
    sync_user_input = SyncsUserInput(
        user_id=str(current_user.id),
        name=name,
        provider="Azure",
        credentials={},
        state={},
        additional_data={},
        status=str(SyncsUserStatus.SYNCING),
    )
    sync_user_service.create_sync_user(sync_user_input)
    return {"authorization_url": f"http://stangirard.com:5050/sync/zendesk/enter-token?state={state}"}

@zendesk_sync_router.get("/sync/zendesk/enter-token", tags=["Sync"])
def enter_zendesk_token_page(request: Request):
    """
    Serve the HTML page to enter the Zendesk API token.
    """
    state = request.query_params.get("state", "")
    zendeskAskTokenPage = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Enter Zendesk API Token</title>
        <style>
            body {{
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                background-color: #f8f9fa;
                font-family: Arial, sans-serif;
            }}
            .container {{
                text-align: center;
                background-color: #fff;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }}
            .input-field {{
                margin-bottom: 20px;
            }}
            .submit-button {{
                padding: 10px 20px;
                font-size: 1em;
                color: #fff;
                background-color: #6142d4;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }}
            .submit-button:hover {{
                background-color: #0056b3;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Enter Your Zendesk API Token</h2>
            <form action="/sync/zendesk/submit-token" method="post">
                <div class="input-field">
                    <input type="text" name="api_token" placeholder="API Token" required>
                </div>
                <input type="hidden" name="state" value="{state}">
                <button type="submit" class="submit-button">Submit</button>
            </form>
        </div>
    </body>
    </html>
    """
    return zendeskAskTokenPage

@zendesk_sync_router.post("/sync/zendesk/submit-token", tags=["Sync"])
def submit_zendesk_token(api_token: str = Form(...), current_user: UserIdentity = Depends(get_current_user)):
    """
    Handle the submission of the Zendesk API token.

    Args:
        api_token (str): The API token provided by the user.
        current_user (UserIdentity): The current authenticated user.

    Returns:
        HTMLResponse: A success page.
    """
    logger.debug(f"Received Zendesk API token for user: {current_user.id}")

    # Update the sync user with the provided Zendesk API token
    sync_user_input = SyncUserUpdateInput(
        email=current_user.email,
        credentials={"api_token": api_token},
        status=str(SyncsUserStatus.SYNCED),
    )
    sync_user_service.update_sync_user(current_user.id, {}, sync_user_input)
    logger.info(f"Zendesk API token updated successfully for user: {current_user.id}")

    return HTMLResponse(successfullConnectionPage)