import os
from typing import List

import msal
import requests
from fastapi import HTTPException
from google.auth.transport.requests import Request as GoogleRequest
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from quivr_api.logger import get_logger
from quivr_api.modules.sync.utils.normalize import remove_special_characters
from requests import HTTPError

logger = get_logger(__name__)


def get_google_drive_files_by_id(credentials: dict, file_ids: List[str]):
    """
    Retrieve files from Google Drive by their IDs.

    Args:
        credentials (dict): The credentials for accessing Google Drive.
        file_ids (list): The list of file IDs to retrieve.

    Returns:
        list: A list of dictionaries containing the metadata of each file or an error message.
    """
    logger.info("Retrieving Google Drive files with file_ids: %s", file_ids)
    creds = Credentials.from_authorized_user_info(credentials)
    if creds.expired and creds.refresh_token:
        creds.refresh(GoogleRequest())
        logger.info("Google Drive credentials refreshed")

    try:
        service = build("drive", "v3", credentials=creds)
        files = []

        for file_id in file_ids:
            result = (
                service.files()
                .get(fileId=file_id, fields="id, name, mimeType, modifiedTime")
                .execute()
            )

            files.append(
                {
                    "name": result["name"],
                    "id": result["id"],
                    "is_folder": result["mimeType"]
                    == "application/vnd.google-apps.folder",
                    "last_modified": result["modifiedTime"],
                    "mime_type": result["mimeType"],
                }
            )

        logger.info("Google Drive files retrieved successfully: %s", len(files))
        for file in files:
            file["name"] = remove_special_characters(file["name"])
        return files
    except HTTPError as error:
        logger.error("An error occurred while retrieving Google Drive files: %s", error)
        return {"error": f"An error occurred: {error}"}


def get_google_drive_files(
    credentials: dict, folder_id: str = None, recursive: bool = False
):
    """
    Retrieve files from Google Drive.

    Args:
        credentials (dict): The credentials for accessing Google Drive.
        folder_id (str, optional): The folder ID to filter files. Defaults to None.
        recursive (bool, optional): If True, fetch files from all subfolders. Defaults to False.

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
        if folder_id:
            query = f"'{folder_id}' in parents"
        else:
            query = "'root' in parents or sharedWithMe"
        page_token = None
        files = []

        while True:
            results = (
                service.files()
                .list(
                    q=query,
                    pageSize=100,
                    fields="nextPageToken, files(id, name, mimeType, modifiedTime)",
                    pageToken=page_token,
                )
                .execute()
            )
            items = results.get("files", [])

            if not items:
                logger.info("No files found in Google Drive")
                break

            for item in items:
                files.append(
                    {
                        "name": item["name"],
                        "id": item["id"],
                        "is_folder": item["mimeType"]
                        == "application/vnd.google-apps.folder",
                        "last_modified": item["modifiedTime"],
                        "mime_type": item["mimeType"],
                    }
                )

                # If recursive is True and the item is a folder, get files from the folder
                if item["name"] == "Monotype":
                    logger.warning(item)
                if (
                    recursive
                    and item["mimeType"] == "application/vnd.google-apps.folder"
                ):
                    logger.warning(
                        "Calling Recursive for folder: %s",
                        item["name"],
                    )
                    files.extend(
                        get_google_drive_files(credentials, item["id"], recursive)
                    )

            page_token = results.get("nextPageToken", None)
            if page_token is None:
                break

        logger.info("Google Drive files retrieved successfully: %s", len(files))

        for file in files:
            file["name"] = remove_special_characters(file["name"])
        return files
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


def list_azure_files(credentials, folder_id=None, recursive=False):
    def fetch_files(endpoint, headers):
        response = requests.get(endpoint, headers=headers)
        if response.status_code == 401:
            token_data = refresh_azure_token(credentials)
            headers = get_azure_headers(token_data)
            response = requests.get(endpoint, headers=headers)
        if response.status_code != 200:
            return {"error": response.text}
        return response.json().get("value", [])

    token_data = get_azure_token_data(credentials)
    headers = get_azure_headers(token_data)
    endpoint = "https://graph.microsoft.com/v1.0/me/drive/root/children"
    if folder_id:
        endpoint = (
            f"https://graph.microsoft.com/v1.0/me/drive/items/{folder_id}/children"
        )

    items = fetch_files(endpoint, headers)

    if not items:
        logger.info("No files found in Azure Drive")
        return []

    files = []
    for item in items:
        file_data = {
            "name": item["name"],
            "id": item["id"],
            "is_folder": "folder" in item,
            "last_modified": item["lastModifiedDateTime"],
            "mime_type": item.get("file", {}).get("mimeType", "folder"),
        }
        files.append(file_data)

        # If recursive option is enabled and the item is a folder, fetch files from it
        if recursive and file_data["is_folder"]:
            folder_files = list_azure_files(
                credentials, folder_id=file_data["id"], recursive=True
            )

            files.extend(folder_files)
    for file in files:
        file["name"] = remove_special_characters(file["name"])
    logger.info("Azure Drive files retrieved successfully: %s", len(files))
    return files


def get_azure_files_by_id(credentials: dict, file_ids: List[str]):
    """
    Retrieve files from Azure Drive by their IDs.

    Args:
        credentials (dict): The credentials for accessing Azure Drive.
        file_ids (list): The list of file IDs to retrieve.

    Returns:
        list: A list of dictionaries containing the metadata of each file or an error message.
    """
    logger.info("Retrieving Azure Drive files with file_ids: %s", file_ids)
    token_data = get_azure_token_data(credentials)
    headers = get_azure_headers(token_data)
    files = []

    for file_id in file_ids:
        endpoint = f"https://graph.microsoft.com/v1.0/me/drive/items/{file_id}"
        response = requests.get(endpoint, headers=headers)
        if response.status_code == 401:
            token_data = refresh_azure_token(credentials)
            headers = get_azure_headers(token_data)
            response = requests.get(endpoint, headers=headers)
        if response.status_code != 200:
            logger.error(
                "An error occurred while retrieving Azure Drive files: %s",
                response.text,
            )
            return {"error": response.text}

        result = response.json()
        files.append(
            {
                "name": result["name"],
                "id": result["id"],
                "is_folder": "folder" in result,
                "last_modified": result["lastModifiedDateTime"],
                "mime_type": result.get("file", {}).get("mimeType", "folder"),
            }
        )

    for file in files:
        file["name"] = remove_special_characters(file["name"])
    logger.info("Azure Drive files retrieved successfully: %s", len(files))
    return files
