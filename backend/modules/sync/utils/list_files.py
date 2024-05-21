import os

import msal
import requests
from fastapi import HTTPException
from google.auth.transport.requests import Request as GoogleRequest
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from logger import get_logger
from requests import HTTPError

logger = get_logger(__name__)


def get_google_drive_files(credentials: dict, folder_id: str = None):
    """
    Retrieve files from Google Drive.

    Args:
        credentials (dict): The credentials for accessing Google Drive.
        folder_id (str, optional): The folder ID to filter files. Defaults to None.

    Returns:
        dict: A dictionary containing the list of files or an error message.
    """
    logger.info("Retrieving Google Drive files with folder_id: %s", folder_id)
    creds = Credentials.from_authorized_user_info(credentials)
    if creds.expired and creds.refresh_token:
        creds.refresh(GoogleRequest())
        logger.info("Google Drive credentials refreshed")
        # Updating the credentials in the database

    try:
        service = build("drive", "v3", credentials=creds)
        query = f"'{folder_id}' in parents" if folder_id else None
        results = (
            service.files()
            .list(
                q=query,
                pageSize=10,
                fields="nextPageToken, files(id, name, mimeType, modifiedTime)",
            )
            .execute()
        )
        items = results.get("files", [])

        if not items:
            logger.info("No files found in Google Drive")
            return {"files": "No files found."}

        files = [
            {
                "name": item["name"],
                "id": item["id"],
                "is_folder": item["mimeType"] == "application/vnd.google-apps.folder",
                "last_modified": item["modifiedTime"],
                "mime_type": item["mimeType"],
            }
            for item in items
        ]
        logger.info("Google Drive files retrieved successfully: %s", files)
        return {"files": files}
    except HTTPError as error:
        logger.error("An error occurred while retrieving Google Drive files: %s", error)
        return {"error": f"An error occurred: {error}"}


CLIENT_ID = os.getenv("SHAREPOINT_CLIENT_ID")
AUTHORITY = "https://login.microsoftonline.com/common"
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:5050")
REDIRECT_URI = f"{BACKEND_URL}/sync/azure/oauth2callback"
SCOPE = [
    "https://graph.microsoft.com/Files.Read",
    "https://graph.microsoft.com/User.Read",
    "https://graph.microsoft.com/Sites.Read.All",
]


def get_azure_token_data(credentials):
    if "access_token" not in credentials:
        raise HTTPException(status_code=401, detail="Invalid token data")
    return credentials


def refresh_azure_token(credentials):
    if "refresh_token" not in credentials:
        raise HTTPException(status_code=401, detail="No refresh token available")

    client = msal.PublicClientApplication(CLIENT_ID, authority=AUTHORITY)
    result = client.acquire_token_by_refresh_token(
        credentials["refresh_token"], scopes=SCOPE
    )
    if "access_token" not in result:
        raise HTTPException(status_code=400, detail="Failed to refresh token")

    return result


def get_azure_headers(token_data):
    return {
        "Authorization": f"Bearer {token_data['access_token']}",
        "Accept": "application/json",
    }


def list_azure_files(credentials, folder_id=None):
    token_data = get_azure_token_data(credentials)
    headers = get_azure_headers(token_data)
    endpoint = f"https://graph.microsoft.com/v1.0/me/drive/root/children"
    if folder_id:
        endpoint = (
            f"https://graph.microsoft.com/v1.0/me/drive/items/{folder_id}/children"
        )
    response = requests.get(endpoint, headers=headers)
    if response.status_code == 401:
        token_data = refresh_azure_token(credentials)
        headers = get_azure_headers(token_data)
        response = requests.get(endpoint, headers=headers)
    if response.status_code != 200:
        return {"error": response.text}
    items = response.json().get("value", [])

    if not items:
        logger.info("No files found in Azure Drive")
        return {"files": "No files found."}

    files = [
        {
            "name": item["name"],
            "id": item["id"],
            "is_folder": "folder" in item,
            "last_modified": item["lastModifiedDateTime"],
            "mime_type": item.get("file", {}).get("mimeType", "folder"),
        }
        for item in items
    ]
    logger.info("Azure Drive files retrieved successfully: %s", files)
    return {"files": files}
