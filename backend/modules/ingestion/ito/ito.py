from tempfile import NamedTemporaryFile
from uuid import UUID

from fastapi import UploadFile
from logger import get_logger
from modules.contact_support.controller.settings import ContactsSettings
from modules.user.entity.user_identity import UserIdentity
from packages.emails.send_email import send_email
from pydantic import BaseModel

logger = get_logger(__name__)


class ITO(BaseModel):
    uploadFile: UploadFile = None
    current_user: UserIdentity = None
    brain_id: UUID = None
    send_file_email: bool = False

    def __init__(
        self,
        uploadFile: UploadFile,
        current_user: UserIdentity,
        brain_id: UUID,
        send_file_email: bool = False,
    ):
        super().__init__(
            uploadFile=uploadFile,
            current_user=current_user,
            brain_id=brain_id,
            send_file_email=send_file_email,
        )

    async def process_ingestion(self):
        pass

    async def send_output_by_email(
        self, file: UploadFile, name: str, custom_message: str = None
    ):
        settings = ContactsSettings()
        file = await self.uploadfile_to_file(file)

        with open(file.name, "rb") as f:

            mail_from = settings.resend_contact_sales_from
            mail_to = self.current_user.email
            body = f"""
            <p>{custom_message}</p>
            """
            params = {
                "from": mail_from,
                "to": mail_to,
                "subject": "Quivr Ingestion Processed",
                "reply_to": "no-reply@quivr.app",
                "html": body,
                "attachments": [{"filename": name, "content": list(f.read())}],
            }
            logger.info(params)
            send_email(params)

    async def uploadfile_to_file(self, uploadFile: UploadFile):
        # Transform the UploadFile object to a file object with same name and content
        tmp_file = NamedTemporaryFile(delete=False)
        tmp_file.write(uploadFile.file.read())
        tmp_file.flush()  # Make sure all data is written to disk
        return tmp_file
