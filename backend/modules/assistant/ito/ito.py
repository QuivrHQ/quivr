import random
from abc import abstractmethod
from io import BytesIO
from tempfile import NamedTemporaryFile
from typing import List

from fastapi import UploadFile
from logger import get_logger
from modules.assistant.dto.inputs import InputAssistant
from modules.contact_support.controller.settings import ContactsSettings
from modules.upload.controller.upload_routes import upload_file
from modules.user.entity.user_identity import UserIdentity
from packages.emails.send_email import send_email
from pydantic import BaseModel

logger = get_logger(__name__)


class ITO(BaseModel):
    input: InputAssistant
    files: List[UploadFile]
    current_user: UserIdentity

    @abstractmethod
    async def process_assistant(self):
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
            logger.info(f"Sending email to {mail_to} with file {name}")
            send_email(params)

    async def uploadfile_to_file(self, uploadFile: UploadFile):
        # Transform the UploadFile object to a file object with same name and content
        tmp_file = NamedTemporaryFile(delete=False)
        tmp_file.write(uploadFile.file.read())
        tmp_file.flush()  # Make sure all data is written to disk
        return tmp_file

    async def create_and_upload_processed_file(
        self, processed_content: str, original_filename: str, file_description: str
    ) -> dict:
        """Handles creation and uploading of the processed file."""
        content_io = BytesIO(processed_content.encode("utf-8"))
        content_io.seek(0)

        new_filename = (
            original_filename.split(".")[0]
            + "_"
            + file_description.lower().replace(" ", "_")
            + "_"
            + str(random.randint(1000, 9999))
            + ".txt"
        )

        file_to_upload = UploadFile(
            filename=new_filename,
            file=content_io,
            headers={"content-type": "text/plain"},
        )

        if self.input.outputs.email.activated:
            await self.send_output_by_email(
                file_to_upload,
                new_filename,
                f"{file_description} of {original_filename}",
            )

        # Reset to start of file before upload
        file_to_upload.file.seek(0)
        if self.input.outputs.brain.activated:
            await upload_file(
                uploadFile=file_to_upload,
                brain_id=self.input.outputs.brain.value,
                current_user=self.current_user,
                chat_id=None,
            )

        return {"message": f"{file_description} generated successfully"}
