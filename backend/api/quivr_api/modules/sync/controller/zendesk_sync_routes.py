import random

from fastapi import APIRouter, Depends, Form, HTTPException, Request
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
def authorize_zendesk(
    request: Request, name: str, current_user: UserIdentity = Depends(get_current_user)
):
    """
    Authorize Zendesk sync for the current user.

    Args:
        request (Request): The request object.
        current_user (UserIdentity): The current authenticated user.

    Returns:
        dict: A dictionary containing the authorization URL.
    """

    state = str(current_user.email) + "," + str(random.randint(100000, 999999))
    sync_user_input = SyncsUserInput(
        user_id=str(current_user.id),
        name=name,
        provider="Zendesk",
        credentials={},
        state={"state": state.split(",")[1]},
        additional_data={},
        status=str(SyncsUserStatus.SYNCING),
    )
    sync_user_service.create_sync_user(sync_user_input)
    return {
        "authorization_url": f"http://localhost:5050/sync/zendesk/enter-token?state={state}"
    }


@zendesk_sync_router.get("/sync/zendesk/enter-token", tags=["Sync"])
def enter_zendesk_token_page(request: Request):
    """
    Serve the HTML page to enter the Zendesk API token and domain name.
    """
    state = request.query_params.get("state", "")
    zendeskAskTokenPage = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Enter Zendesk API Token and Domain</title>
        <style>
            body {{
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                background-color: #f0f2f5;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }}
            .container {{
                text-align: center;
                background-color: #ffffff;
                padding: 40px;
                border-radius: 12px;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
                width: 400px;
            }}
            .input-field {{
                margin-bottom: 24px;
                text-align: left;
            }}
            .input-field input {{
                width: 100%;
                padding: 12px;
                border: 1px solid #d1d5db;
                border-radius: 6px;
                font-size: 16px;
                transition: border-color 0.3s ease;
            }}
            .input-field input:focus {{
                outline: none;
                border-color: #6142d4;
            }}
            .submit-button {{
                width: 100%;
                padding: 12px;
                font-size: 16px;
                font-weight: bold;
                color: #ffffff;
                background-color: #6142d4;
                border: none;
                border-radius: 6px;
                cursor: pointer;
                transition: background-color 0.3s ease;
            }}
            .submit-button:hover {{
                background-color: #4e35a8;
            }}
            .domain-suffix {{
                display: block;
                margin-top: 8px;
                font-size: 14px;
                color: #6b7280;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Enter Your Zendesk API Token and Domain</h2>
            <form action="/sync/zendesk/submit-token" method="post">
                <div class="input-field">
                    <input type="text" name="email" placeholder="Zendesk Email" required>
                </div>
                <div class="input-field">
                    <input type="text" name="sub_domain_name" placeholder="Sub Domain Name" required>
                    <span class="domain-suffix">.zendesk.com</span>
                </div>
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
    return HTMLResponse(content=zendeskAskTokenPage, status_code=200)


@zendesk_sync_router.post("/sync/zendesk/submit-token", tags=["Sync"])
def submit_zendesk_token(
    api_token: str = Form(...),
    sub_domain_name: str = Form(...),
    email: str = Form(...),
    state: str = Form(...),
):
    """
    Handle the submission of the Zendesk API token.

    Args:
        api_token (str): The API token provided by the user.
        current_user (UserIdentity): The current authenticated user.

    Returns:
        HTMLResponse: A success page.
    """
    user_email, sync_state = state.split(",")
    state_dict = {"state": sync_state}
    logger.debug(f"Handling OAuth2 callback for user with state: {state}")
    sync_user_state = sync_user_service.get_sync_user_by_state(state_dict)
    logger.info(f"Retrieved sync user state: {sync_user_state}")
    if not sync_user_state or state_dict != sync_user_state.state:
        logger.error("Invalid state parameter")
        raise HTTPException(status_code=400, detail="Invalid state parameter")

    logger.debug(
        f"Received Zendesk API token and sub domain name for user: {sync_user_state.user_id}"
    )
    assert email is not None, "User email is None"

    # Update the sync user with the provided Zendesk API token
    sync_user_input = SyncUserUpdateInput(
        email=email,
        credentials={
            "api_token": api_token,
            "sub_domain_name": sub_domain_name,
            "email": email,
        },
        status=str(SyncsUserStatus.SYNCED),
    )
    sync_user_service.update_sync_user(
        sync_user_state.user_id, state_dict, sync_user_input
    )
    logger.info(
        f"Zendesk API token updated successfully for user: {sync_user_state.user_id}"
    )

    return HTMLResponse(successfullConnectionPage)
