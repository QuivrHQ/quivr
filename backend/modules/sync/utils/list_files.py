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
