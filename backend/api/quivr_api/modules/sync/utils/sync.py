import json
import os
import time
from abc import ABC, abstractmethod
from datetime import datetime
from io import BytesIO
from typing import Any, Dict, List, Union

import dropbox
import msal
import requests
from fastapi import HTTPException
from google.auth.transport.requests import Request as GoogleRequest
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from requests import HTTPError

from quivr_api.logger import get_logger
from quivr_api.modules.sync.entity.sync import SyncFile
from quivr_api.modules.sync.utils.normalize import remove_special_characters

logger = get_logger(__name__)


class BaseSync(ABC):
    name: str
    lower_name: str
    datetime_format: str

    @abstractmethod
    def get_files_by_id(self, credentials: Dict, file_ids: List[str]) -> List[SyncFile]:
        raise NotImplementedError

    @abstractmethod
    def get_files(
        self, credentials: Dict, folder_id: str | None = None, recursive: bool = False
    ) -> List[SyncFile]:
        raise NotImplementedError

    @abstractmethod
    def check_and_refresh_access_token(self, credentials: dict) -> Dict:
        raise NotImplementedError

    @abstractmethod
    def download_file(
        self, credentials: Dict, file: SyncFile
    ) -> Dict[str, Union[str, BytesIO]]:
        raise NotImplementedError


class GoogleDriveSync(BaseSync):
    name = "Google Drive"
    lower_name = "google"
    creds: Credentials | None = None
    service: Any | None = None
    datetime_format: str = "%Y-%m-%dT%H:%M:%S.%fZ"

    def check_and_refresh_access_token(self, credentials: dict) -> Dict:
        self.creds = Credentials.from_authorized_user_info(credentials)
        if self.creds.expired and self.creds.refresh_token:
            self.creds.refresh(GoogleRequest())
            logger.info("Google Drive credentials refreshed")
        return json.loads(self.creds.to_json())

    def download_file(
        self, credentials: Dict, file: SyncFile
    ) -> Dict[str, Union[str, BytesIO]]:
        file_id = file.id
        file_name = file.name
        mime_type = file.mime_type
        if not self.creds:
            self.check_and_refresh_access_token(credentials)
        if not self.service:
            self.service = build("drive", "v3", credentials=self.creds)

        # Convert Google Docs files to appropriate formats before downloading
        if mime_type == "application/vnd.google-apps.document":
            logger.debug(
                "Converting Google Docs file with file_id: %s to DOCX.",
                file_id,
            )
            request = self.service.files().export_media(
                fileId=file_id,
                mimeType="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
            file_name += ".docx"
        elif mime_type == "application/vnd.google-apps.spreadsheet":
            logger.debug(
                "Converting Google Sheets file with file_id: %s to XLSX.",
                file_id,
            )
            request = self.service.files().export_media(
                fileId=file_id,
                mimeType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
            file_name += ".xlsx"
        elif mime_type == "application/vnd.google-apps.presentation":
            logger.debug(
                "Converting Google Slides file with file_id: %s to PPTX.",
                file_id,
            )
            request = self.service.files().export_media(
                fileId=file_id,
                mimeType="application/vnd.openxmlformats-officedocument.presentationml.presentation",
            )
            file_name += ".pptx"
        ### Elif pdf, txt, md, csv, docx, xlsx, pptx, doc
        elif file_name.split(".")[-1] in [
            "pdf",
            "txt",
            "md",
            "csv",
            "docx",
            "xlsx",
            "pptx",
            "doc",
        ]:
            request = self.service.files().get_media(fileId=file_id)
        else:
            logger.warning(
                "Skipping unsupported file type: %s for file_id: %s",
                mime_type,
                file_id,
            )
            raise Exception("Unsupported file type")

        file_data = request.execute()
        return {"file_name": file_name, "content": BytesIO(file_data)}

    def get_files_by_id(self, credentials: Dict, file_ids: List[str]) -> List[SyncFile]:
        """
        Retrieve files from Google Drive by their IDs.

        Args:
            credentials (dict): The credentials for accessing Google Drive.
            file_ids (list): The list of file IDs to retrieve.

        Returns:
            list: A list of dictionaries containing the metadata of each file or an error message.
        """
        logger.info("Retrieving Google Drive files with file_ids: %s", file_ids)
        self.check_and_refresh_access_token(credentials)

        try:
            service = build("drive", "v3", credentials=self.creds)
            files: List[SyncFile] = []

            for file_id in file_ids:
                result = (
                    service.files()
                    .get(
                        fileId=file_id,
                        fields="id, name, mimeType, modifiedTime, webViewLink",
                    )
                    .execute()
                )

                files.append(
                    SyncFile(
                        name=result["name"],
                        id=result["id"],
                        is_folder=(
                            result["mimeType"] == "application/vnd.google-apps.folder"
                        ),
                        last_modified=result["modifiedTime"],
                        mime_type=result["mimeType"],
                        web_view_link=result["webViewLink"],
                    )
                )

            logger.info("Google Drive files retrieved successfully: %s", len(files))
            for file in files:
                file.name = remove_special_characters(file.name)
            return files

        except HTTPError as error:
            logger.error(
                "An error occurred while retrieving Google Drive files: %s", error
            )
            raise Exception("Failed to retrieve files")

    def get_files(
        self, credentials: dict, folder_id: str | None = None, recursive: bool = False
    ) -> List[SyncFile]:
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

        self.check_and_refresh_access_token(credentials)
        # Updating the credentials in the database

        try:
            service = build("drive", "v3", credentials=self.creds)
            if folder_id:
                query = f"'{folder_id}' in parents"
            else:
                query = "'root' in parents or sharedWithMe"
            page_token = None
            files: List[SyncFile] = []

            while True:
                results = (
                    service.files()
                    .list(
                        q=query,
                        pageSize=100,
                        fields="nextPageToken, files(id, name, mimeType, modifiedTime, webViewLink)",
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
                        SyncFile(
                            name=item["name"],
                            id=item["id"],
                            is_folder=(
                                item["mimeType"] == "application/vnd.google-apps.folder"
                            ),
                            last_modified=item["modifiedTime"],
                            mime_type=item["mimeType"],
                            web_view_link=item["webViewLink"],
                        )
                    )

                    # If recursive is True and the item is a folder, get files from the folder
                    if (
                        recursive
                        and item["mimeType"] == "application/vnd.google-apps.folder"
                    ):
                        logger.warning(
                            "Calling Recursive for folder: %s",
                            item["name"],
                        )
                        files.extend(self.get_files(credentials, item["id"], recursive))

                page_token = results.get("nextPageToken", None)
                if page_token is None:
                    break

            logger.info("Google Drive files retrieved successfully: %s", len(files))

            for file in files:
                file.name = remove_special_characters(file.name)
            return files
        except HTTPError as error:
            logger.error(
                "An error occurred while retrieving Google Drive files: %s", error
            )
            raise Exception("Failed to retrieve files")


class AzureDriveSync(BaseSync):
    name = "Share Point"
    lower_name = "azure"
    datetime_format: str = "%Y-%m-%dT%H:%M:%SZ"
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

    @staticmethod
    def get_azure_token_data(credentials):
        if "access_token" not in credentials:
            raise HTTPException(status_code=401, detail="Invalid token data")
        return credentials

    @staticmethod
    def get_azure_headers(token_data):
        return {
            "Authorization": f"Bearer {token_data['access_token']}",
            "Accept": "application/json",
        }

    def check_and_refresh_access_token(self, credentials) -> Dict:
        if "refresh_token" not in credentials:
            raise HTTPException(status_code=401, detail="No refresh token available")

        client = msal.ConfidentialClientApplication(
            self.CLIENT_ID,
            authority=self.AUTHORITY,
            client_credential=self.CLIENT_SECRET,
        )
        result = client.acquire_token_by_refresh_token(
            credentials["refresh_token"], scopes=self.SCOPE
        )
        if "access_token" not in result:
            raise HTTPException(
                status_code=400, detail=f"Failed to refresh token: {result}"
            )

        credentials.update(
            {
                "access_token": result["access_token"],
                "refresh_token": result.get(
                    "refresh_token", credentials["refresh_token"]
                ),
                "id_token": result.get("id_token", credentials.get("id_token")),
            }
        )

        return credentials

    def get_files(
        self, credentials, site_folder_id=None, recursive=False
    ) -> List[SyncFile]:
        def fetch_files(endpoint, headers, max_retries=1):
            logger.debug(f"fetching files from {endpoint}.")

            retry_count = 0
            while retry_count <= max_retries:
                try:
                    response = requests.get(endpoint, headers=headers)

                    # Retrying with refereshed token
                    if response.status_code == 401:
                        token_data = self.check_and_refresh_access_token(credentials)
                        headers = self.get_azure_headers(token_data)
                        response = requests.get(endpoint, headers=headers)
                    else:
                        response.raise_for_status()
                    return response.json().get("value", [])

                except HTTPError as e:
                    logger.exception(
                        f"azure_list_files got exception : {e}. headers: {headers}. {retry_count} retrying."
                    )
                    # Exponential backoff
                    time.sleep(2**retry_count)
                    retry_count += 1

            raise HTTPException(
                504, detail="can't connect to azure endpoint to retrieve files."
            )

        token_data = self.get_azure_token_data(credentials)
        headers = self.get_azure_headers(token_data)
        if not site_folder_id:
            folder_id = None
            site_id = None
        else:
            site_id, folder_id = site_folder_id.split(":")
            if folder_id == "":
                folder_id = None

        if not folder_id and not site_id:
            # Fetch the sites
            # endpoint = "https://graph.microsoft.com/v1.0/me/followedSites"
            endpoint = "https://graph.microsoft.com/v1.0/sites?search=*"
        elif site_id == "root":
            if not folder_id:
                endpoint = "https://graph.microsoft.com/v1.0/me/drive/root/children"
            else:
                endpoint = f"https://graph.microsoft.com/v1.0/me/drive/items/{folder_id}/children"
        else:
            if not folder_id:
                endpoint = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drive/root/children"
            else:
                endpoint = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drive/items/{folder_id}/children"
        items = fetch_files(endpoint, headers)

        if not folder_id and not site_id and len(items) == 0:
            logger.debug("No sites found in Azure Drive, files : %s", items)
            return self.get_files(credentials, "root:", recursive)

        if not items:
            logger.info("No files found in Azure Drive")
            return []
        else:
            logger.info("Azure Drive files found: %s", items)

        files = []
        for item in items:
            file_data = SyncFile(
                name=item.get("name") if site_folder_id else item.get("displayName"),
                id=f'{item.get("id", {}).split(",")[1]}:'
                if not site_folder_id
                else f'{site_id}:{item.get("id")}',
                is_folder="folder" in item or not site_folder_id,
                last_modified=item.get("lastModifiedDateTime"),
                mime_type=item.get("file", {}).get("mimeType", "folder"),
                web_view_link=item.get("webUrl"),
            )
            files.append(file_data)

            # If recursive option is enabled and the item is a folder, fetch files from it
            if recursive and file_data.is_folder:
                folder_files = self.get_files(
                    credentials, site_folder_id=file_data.id, recursive=True
                )

                files.extend(folder_files)
        if not folder_id and not site_id:
            files.append(
                SyncFile(
                    name="My Drive",
                    id="root:",
                    is_folder=True,
                    last_modified="",
                    mime_type="folder",
                    web_view_link="https://onedrive.live.com",
                )
            )
        for file in files:
            file.name = remove_special_characters(file.name)
        logger.info("Azure Drive files retrieved successfully: %s", len(files))
        return files

    def get_files_by_id(self, credentials: dict, file_ids: List[str]) -> List[SyncFile]:
        """
        Retrieve files from Azure Drive by their IDs.

        Args:
            credentials (dict): The credentials for accessing Azure Drive.
            file_ids (list): The list of file IDs to retrieve.

        Returns:
            list: A list of dictionaries containing the metadata of each file or an error message.
        """
        logger.info("Retrieving Azure Drive files with file_ids: %s", file_ids)
        token_data = self.get_azure_token_data(credentials)
        headers = self.get_azure_headers(token_data)
        files = []

        for file_id in file_ids:
            site_id, folder_id = file_id.split(":")
            if folder_id == "":
                folder_id = None
            if site_id == "root":
                endpoint = (
                    f"https://graph.microsoft.com/v1.0/me/drive/items/{folder_id}"
                )
            else:
                endpoint = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drive/items/{folder_id}"
            response = requests.get(endpoint, headers=headers)
            if response.status_code == 401:
                token_data = self.check_and_refresh_access_token(credentials)
                headers = self.get_azure_headers(token_data)
                response = requests.get(endpoint, headers=headers)
            if response.status_code != 200:
                logger.error(
                    "An error occurred while retrieving Azure Drive files: %s",
                    response.text,
                )
                raise Exception("Failed to retrieve files")

            result = response.json()
            files.append(
                SyncFile(
                    name=result.get("name"),
                    id=f'{site_id}:{result.get("id")}',
                    is_folder="folder" in result,
                    last_modified=result.get("lastModifiedDateTime"),
                    mime_type=result.get("file", {}).get("mimeType", "folder"),
                    web_view_link=result.get("webUrl"),
                )
            )

        for file in files:
            file.name = remove_special_characters(file.name)
        logger.info("Azure Drive files retrieved successfully: %s", len(files))
        return files

    def download_file(
        self, credentials: Dict, file: SyncFile
    ) -> Dict[str, Union[str, BytesIO]]:
        file_id = file.id
        file_name = file.name
        headers = self.get_azure_headers(credentials)
        site_id, folder_id = file_id.split(":")
        if folder_id == "":
            folder_id = None
        if site_id == "root":
            download_endpoint = (
                f"https://graph.microsoft.com/v1.0/me/drive/items/{file_id}/content"
            )
        else:
            download_endpoint = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drive/items/{folder_id}/content"
        logger.info("Downloading file: %s", file_name)
        download_response = requests.get(
            download_endpoint, headers=headers, stream=True
        )
        return {"file_name": file_name, "content": BytesIO(download_response.content)}


class DropboxSync(BaseSync):
    name = "Dropbox"
    lower_name = "dropbox"
    dbx: dropbox.Dropbox | None = None
    datetime_format: str = "%Y-%m-%d %H:%M:%S"

    def link_dropbox(self, credentials) -> dropbox.Dropbox:
        return dropbox.Dropbox(
            credentials["access_token"],
            oauth2_refresh_token=credentials["refresh_token"],
            app_key=os.getenv("DROPBOX_APP_KEY"),
            oauth2_access_token_expiration=credentials.get("expires_at"),
            app_secret=os.getenv("DROPBOX_APP_SECRET"),
        )

    def check_and_refresh_access_token(self, credentials: Dict) -> Dict:
        if not self.dbx:
            self.dbx = self.link_dropbox(credentials)
        self.dbx.check_and_refresh_access_token()
        credentials["access_token"] = self.dbx._oauth2_access_token
        credentials["refresh_token"] = self.dbx.refresh_access_token
        return credentials

    def get_files(
        self, credentials: Dict, folder_id: str = "", recursive: bool = False
    ) -> List[SyncFile]:
        """
        Retrieve files from Dropbox.

        Args:
            credentials (dict): The credentials for accessing Dropbox.
            folder_id (str, optional): The folder ID to filter files. Defaults to "".
            recursive (bool, optional): If True, fetch files from all subfolders. Defaults to False.

        Returns:
            dict: A dictionary containing the list of files or an error message.
        """
        logger.info("Retrieving Dropbox files with folder_id: %s", folder_id)

        # Verify credential has the access token
        if "access_token" not in credentials:
            logger.error("Invalid access token")
            raise Exception("Invalid access token")

        try:
            if not self.dbx:
                self.dbx = dropbox.Dropbox(
                    credentials["access_token"],
                    oauth2_refresh_token=credentials["refresh_token"],
                    app_key=os.getenv("DROPBOX_APP_KEY"),
                    oauth2_access_token_expiration=credentials.get("expires_at"),
                    app_secret=os.getenv("DROPBOX_APP_SECRET"),
                )
            self.dbx.check_and_refresh_access_token()
            credentials["access_token"] = self.dbx._oauth2_access_token

            def fetch_files(metadata):
                files = []
                for file in metadata.entries:
                    shared_link = f"https://www.dropbox.com/preview{file.path_display}?context=content_suggestions&role=personal"
                    is_folder = isinstance(file, dropbox.files.FolderMetadata)

                    files.append(
                        SyncFile(
                            name=file.name,
                            id=file.id,
                            is_folder=is_folder,
                            last_modified=(
                                str(file.client_modified) if not is_folder else ""
                            ),
                            mime_type=(
                                file.path_lower.split(".")[-1] if not is_folder else ""
                            ),
                            web_view_link=shared_link,
                        )
                    )
                return files

            files = []
            list_metadata = self.dbx.files_list_folder(folder_id, recursive=recursive)
            files.extend(fetch_files(list_metadata))

            while list_metadata.has_more:
                list_metadata = self.dbx.files_list_folder_continue(
                    list_metadata.cursor
                )
                files.extend(fetch_files(list_metadata))

            for file in files:
                file.name = remove_special_characters(file.name)

            logger.info("Dropbox files retrieved successfully: %d", len(files))
            return files

        except dropbox.exceptions.ApiError as e:
            logger.error("Dropbox API error: %s", e)
            raise Exception("Failed to retrieve files")
        except Exception as e:
            logger.error("Unexpected error: %s", e)
            raise Exception("Failed to retrieve files")

    def get_files_by_id(
        self, credentials: Dict[str, str], file_ids: List[str]
    ) -> List[SyncFile]:
        """
        Retrieve files from Dropbox by their IDs.

        Args:
            credentials (dict): The credentials for accessing Dropbox.
            file_ids (list): The list of file IDs to retrieve.

        Returns:
            list: A list of dictionaries containing the metadata of each file or an error message.
        """
        logger.info("Retrieving Dropbox files with file_ids: %s", file_ids)

        if "access_token" not in credentials:
            logger.error("Access token is not in the credentials")
            raise Exception("Invalid access token")

        try:
            if not self.dbx:
                self.dbx = self.link_dropbox(credentials)
            self.dbx.check_and_refresh_access_token()
            credentials["access_token"] = self.dbx._oauth2_access_token  # type: ignore

            files = []

            for file_id in file_ids:
                try:
                    metadata = self.dbx.files_get_metadata(file_id)
                    shared_link = f"https://www.dropbox.com/preview/{metadata.path_display}?context=content_suggestions&role=personal"
                    is_folder = isinstance(metadata, dropbox.files.FolderMetadata)
                    file_info = SyncFile(
                        name=metadata.name,
                        id=metadata.id,
                        is_folder=is_folder,
                        last_modified=(
                            str(metadata.client_modified) if not is_folder else ""
                        ),
                        mime_type=(
                            metadata.path_lower.split(".")[-1] if not is_folder else ""
                        ),
                        web_view_link=shared_link,
                    )

                    files.append(file_info)
                except dropbox.exceptions.ApiError as api_err:
                    logger.error(
                        "Dropbox API error for file_id %s: %s", file_id, api_err
                    )
                    continue  # Skip this file and proceed with the next one
                except Exception as err:
                    logger.error("Unexpected error for file_id %s: %s", file_id, err)
                    continue  # Skip this file and proceed with the next one

            for file in files:
                file.name = remove_special_characters(file.name)

            logger.info("Dropbox files retrieved successfully: %d", len(files))
            return files

        except dropbox.exceptions.AuthError as auth_err:
            logger.error("Authentication error: %s", auth_err)
            raise Exception("Failed to retrieve files")
        except Exception as e:
            logger.error("Unexpected error: %s", e)
            raise Exception("Failed to retrieve files")

    def download_file(
        self, credentials: Dict, file: SyncFile
    ) -> Dict[str, Union[str, BytesIO]]:
        file_id = str(file.id)
        file_name = file.name
        if not self.dbx:
            self.dbx = self.link_dropbox(credentials)

        metadata, file_data = self.dbx.files_download(file_id)  # type: ignore
        return {"file_name": file_name, "content": BytesIO(file_data.content)}


class GitHubSync(BaseSync):
    name = "GitHub"
    lower_name = "github"
    datetime_format = "%Y-%m-%dT%H:%M:%SZ"

    def __init__(self):
        self.CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
        self.CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
        self.BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:5050")
        self.REDIRECT_URI = f"{self.BACKEND_URL}/sync/github/oauth2callback"
        self.SCOPE = "repo user"

    def get_github_token_data(self, credentials):
        if "access_token" not in credentials:
            raise HTTPException(status_code=401, detail="Invalid token data")
        return credentials

    def get_github_headers(self, token_data):
        return {
            "Authorization": f"Bearer {token_data['access_token']}",
            "Accept": "application/json",
        }

    def check_and_refresh_access_token(self, credentials: dict) -> Dict:
        # GitHub tokens do not support refresh token, usually need to re-authenticate
        raise HTTPException(
            status_code=400, detail="GitHub does not support token refresh"
        )

    def get_files(
        self, credentials: Dict, folder_id: str | None = None, recursive: bool = False
    ) -> List[SyncFile]:
        logger.info("Retrieving GitHub files with folder_id: %s", folder_id)
        if folder_id:
            return self.list_github_files_in_repo(
                credentials, folder_id, recursive=recursive
            )
        else:
            return self.list_github_repos(credentials, recursive=recursive)

    def get_files_by_id(self, credentials: Dict, file_ids: List[str]) -> List[SyncFile]:
        token_data = self.get_github_token_data(credentials)
        headers = self.get_github_headers(token_data)
        files = []

        for file_id in file_ids:
            repo_name, file_path = file_id.split(":")
            endpoint = f" https://api.github.com/repos/{repo_name}/contents/{file_path}"
            response = requests.get(endpoint, headers=headers)
            if response.status_code == 401:
                raise HTTPException(status_code=401, detail="Unauthorized")
            if response.status_code != 200:
                logger.error(
                    "An error occurred while retrieving GitHub files: %s", response.text
                )
                raise Exception("Failed to retrieve files")

            result = response.json()
            logger.debug("GitHub file result: %s", result)
            files.append(
                SyncFile(
                    name=remove_special_characters(result.get("name")),
                    id=f"{repo_name}:{result.get('path')}",
                    is_folder=False,
                    last_modified=datetime.now().strftime(self.datetime_format),
                    mime_type=result.get("type"),
                    web_view_link=result.get("html_url"),
                )
            )

        logger.info("GitHub files retrieved successfully: %s", len(files))
        return files

    def download_file(
        self, credentials: Dict, file: SyncFile
    ) -> Dict[str, Union[str, BytesIO]]:
        token_data = self.get_github_token_data(credentials)
        headers = self.get_github_headers(token_data)
        project_name, file_path = file.id.split(":")

        # Construct the API endpoint for the file content
        endpoint = f"https://api.github.com/repos/{project_name}/contents/{file_path}"

        response = requests.get(endpoint, headers=headers)
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code, detail="Failed to download file"
            )

        content = response.json().get("content")
        if not content:
            raise HTTPException(status_code=404, detail="File content not found")

        # GitHub API returns content as base64 encoded string
        import base64

        file_content = base64.b64decode(content)

        return {"file_name": file.name, "content": BytesIO(file_content)}

    def list_github_repos(self, credentials, recursive=False):
        def fetch_repos(endpoint, headers):
            response = requests.get(endpoint, headers=headers)
            if response.status_code == 401:
                raise HTTPException(status_code=401, detail="Unauthorized")
            if response.status_code != 200:
                logger.error(
                    "An error occurred while retrieving GitHub repositories: %s",
                    response.text,
                )
                return []
            return response.json()

        token_data = self.get_github_token_data(credentials)
        headers = self.get_github_headers(token_data)
        endpoint = "https://api.github.com/user/repos"

        items = fetch_repos(endpoint, headers)

        if not items:
            logger.info("No repositories found in GitHub")
            return []

        repos = []
        for item in items:
            repo_data = SyncFile(
                name=remove_special_characters(item.get("name")),
                id=f"{item.get('full_name')}:",
                is_folder=True,
                last_modified=str(item.get("updated_at")),
                mime_type="repository",
                web_view_link=item.get("html_url"),
            )
            repos.append(repo_data)

            if recursive:
                submodule_files = self.list_github_files_in_repo(
                    credentials, repo_data.id
                )
                repos.extend(submodule_files)

        logger.info("GitHub repositories retrieved successfully: %s", len(repos))
        return repos

    def list_github_files_in_repo(self, credentials, repo_folder, recursive=False):
        def fetch_files(endpoint, headers):
            response = requests.get(endpoint, headers=headers)
            if response.status_code == 401:
                raise HTTPException(status_code=401, detail="Unauthorized")
            if response.status_code != 200:
                logger.error(
                    "An error occurred while retrieving GitHub repository files: %s",
                    response.text,
                )
                return []
            return response.json()

        repo_name, folder_path = repo_folder.split(":")
        token_data = self.get_github_token_data(credentials)
        headers = self.get_github_headers(token_data)
        endpoint = f"https://api.github.com/repos/{repo_name}/contents/{folder_path}"
        logger.debug(f"Fetching files from GitHub with link: {endpoint}")

        items = fetch_files(endpoint, headers)

        if not items:
            logger.info(f"No files found in GitHub repository {repo_name}")
            return []

        files = []
        for item in items:
            file_data = SyncFile(
                name=remove_special_characters(item.get("name")),
                id=f"{repo_name}:{item.get('path')}",
                is_folder=item.get("type") == "dir",
                last_modified=str(item.get("updated_at")),
                mime_type=item.get("type"),
                web_view_link=item.get("html_url"),
            )
            files.append(file_data)

            if recursive and file_data.is_folder:
                folder_files = self.list_github_files_in_repo(
                    credentials, repo_folder=file_data.id, recursive=True
                )
                files.extend(folder_files)

        logger.info(f"GitHub repository files retrieved successfully: {len(files)}")
        return files
