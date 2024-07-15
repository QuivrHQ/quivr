import os

import dropbox
from dropbox import DropboxOAuth2FlowNoRedirect
from quivr_api.logger import get_logger

logger = get_logger(__name__)

APP_KEY = os.getenv("DROPBOX_APP_KEY")
APP_SECRET = os.getenv("DROPBOW_CONSUMER_SECRET")


class DropboxSyncUtils:
    def refresh_token(self, refresh_token):
        """
        Refresh the access token for DropBox.

        Args:
            refresh_token (str): The refresh token for DropBox.

        Returns:
            dict: The new access token.
        """
        auth_flow = DropboxOAuth2FlowNoRedirect(
            APP_KEY,
            consumer_secret=APP_SECRET,
            token_access_type="offline",
            scope=["files.metadata.read"],
        )
        authorize_url = auth_flow.start()
        auth_code = input("Enter the authorization code here: ").strip()

        try:
            oauth_result = auth_flow.finish(auth_code)
            assert oauth_result.scope == "files.metadata.read"
            return oauth_result
        except Exception as e:
            logger.error(f"Error: {e}")

        with dropbox.Dropbox(
            oauth2_access_token=oauth_result.access_token,
            oauth2_access_token_expiration=oauth_result.expires_at,
            oauth2_refresh_token=oauth_result.refresh_token,
            app_key=APP_KEY,
            app_secret=APP_SECRET,
        ) as dbx:

            dbx.users_get_current_account()
            print("Successfully set up client!")

    async def _upload_files(
        self,
        token_data: dict,
        files: list,
        current_user: str,
        brain_id: str,
        sync_active_id: int,
    ):
        """
        Download files from DropBox.

        Args:
            credentials (dict): The credentials for accessing Google Drive.
            files (list): The list of file metadata to download.

        Returns:
            dict: A dictionary containing the status of the download or an error message.
        """
        pass

    async def sync(self, sync_active_id: int, user_id: str):
        """
        Check if the Dropbox sync has not been synced and download the folders and files based on the settings.

        Args:
            sync_active_id (int): The ID of the active sync.
            user_id (str): The user ID associated with the active sync.
        """
        pass
