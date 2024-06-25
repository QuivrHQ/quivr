import os
import random
import re
import string
from abc import abstractmethod
from io import BytesIO
from tempfile import NamedTemporaryFile
from typing import List, Optional

from fastapi import UploadFile
from logger import get_logger
from modules.assistant.dto.inputs import InputAssistant
from modules.assistant.ito.utils.pdf_generator import PDFGenerator, PDFModel
from modules.chat.controller.chat.utils import update_user_usage
from modules.contact_support.controller.settings import ContactsSettings
from modules.notification.dto.inputs import NotificationUpdatableProperties
from modules.notification.entity.notification import NotificationsStatusEnum
from modules.notification.service.notification_service import NotificationService
from modules.upload.controller.upload_routes import upload_file
from modules.user.entity.user_identity import UserIdentity
from modules.user.service.user_usage import UserUsage
from packages.emails.send_email import send_email
from pydantic import BaseModel
from unidecode import unidecode

logger = get_logger(__name__)

notification_service = NotificationService()


class ITO(BaseModel):
    input: InputAssistant
    files: List[UploadFile]
    current_user: UserIdentity
    user_usage: Optional[UserUsage] = None
    user_settings: Optional[dict] = None

    def __init__(
        self,
        input: InputAssistant,
        files: List[UploadFile] = None,
        current_user: UserIdentity = None,
        **kwargs,
    ):
        super().__init__(
            input=input,
            files=files,
            current_user=current_user,
            **kwargs,
        )
        self.user_usage = UserUsage(
            id=current_user.id,
            email=current_user.email,
        )
        self.user_settings = self.user_usage.get_user_settings()
        self.increase_usage_user()

    def increase_usage_user(self):
        # Raises an error if the user has consumed all of of his credits

        update_user_usage(
            usage=self.user_usage,
            user_settings=self.user_settings,
            cost=self.calculate_pricing(),
        )

    def calculate_pricing(self):
        return 20

    @abstractmethod
    async def process_assistant(self):
        pass


async def uploadfile_to_file(uploadFile: UploadFile):
    # Transform the UploadFile object to a file object with same name and content
    tmp_file = NamedTemporaryFile(delete=False)
    tmp_file.write(uploadFile.file.read())
    tmp_file.flush()  # Make sure all data is written to disk
    return tmp_file


class OutputHandler(BaseModel):
    async def send_output_by_email(
        self,
        filename: str,
        file: UploadFile,
        task_name: str,
        custom_message: str,
        brain_id: str = None,
        user_email: str = None,
    ):
        settings = ContactsSettings()
        file = await uploadfile_to_file(file)
        domain_quivr = os.getenv("QUIVR_DOMAIN", "https://chat.quivr.app/")

        with open(file.name, "rb") as f:
            mail_from = settings.resend_contact_sales_from
            mail_to = user_email
            body = f"""
            <div style="text-align: center;">
                <img src="https://quivr-cms.s3.eu-west-3.amazonaws.com/logo_quivr_white_7e3c72620f.png" alt="Quivr Logo" style="width: 100px; height: 100px; border-radius: 50%; margin: 0 auto; display: block;">
                
                <p>Quivr's ingestion process has been completed. The processed file is attached.</p>
                
                <p><strong>Task:</strong> {task_name}</p>
                
                <p><strong>Output:</strong> {custom_message}</p>
                <br />
                

            </div>
            """
            if brain_id:
                body += f"<div style='text-align: center;'>You can find the file <a href='{domain_quivr}studio/{brain_id}'>here</a>.</div> <br />"
            body += f"""
            <div style="text-align: center;">
                <p>Please let us know if you have any questions or need further assistance.</p>
                
                <p> The Quivr Team </p>
            </div>
            """
            params = {
                "sender": mail_from,
                "to": [mail_to],
                "subject": "Quivr Ingestion Processed",
                "reply_to": "no-reply@quivr.app",
                "html": body,
                "attachments": [
                    {
                        "filename": filename,
                        "content": list(f.read()),
                        "type": "application/pdf",
                    }
                ],
            }
            logger.info(f"Sending email to {mail_to} with file {filename}")
            send_email(params)

    def generate_pdf(self, filename: str, title: str, content: str):
        pdf_model = PDFModel(title=title, content=content)
        pdf = PDFGenerator(pdf_model)
        pdf.print_pdf()
        pdf.output(filename, "F")

    async def create_and_upload_processed_file(
        self,
        processed_content: str,
        original_filename: str,
        file_description: str,
        content: str,
        task_name: str,
        custom_message: str,
        brain_id: str = None,
        email_activated: bool = False,
        current_user: UserIdentity = None,
        notification_id: str = None,
    ) -> dict:
        """Handles creation and uploading of the processed file."""
        # remove any special characters from the filename that aren't http safe

        new_filename = (
            original_filename.split(".")[0]
            + "_"
            + file_description.lower().replace(" ", "_")
            + "_"
            + str(random.randint(1000, 9999))
            + ".pdf"
        )
        new_filename = unidecode(new_filename)
        new_filename = re.sub(
            "[^{}0-9a-zA-Z]".format(re.escape(string.punctuation)), "", new_filename
        )

        self.generate_pdf(
            new_filename,
            f"{file_description} of {original_filename}",
            processed_content,
        )

        content_io = BytesIO()
        with open(new_filename, "rb") as f:
            content_io.write(f.read())
        content_io.seek(0)

        file_to_upload = UploadFile(
            filename=new_filename,
            file=content_io,
            headers={"content-type": "application/pdf"},
        )

        logger.info(f"current_user: {current_user}")
        if email_activated:
            await self.send_output_by_email(
                new_filename,
                file_to_upload,
                "Summary",
                f"{file_description} of {original_filename}",
                brain_id=brain_id,
                user_email=current_user["email"],
            )

        # Reset to start of file before upload
        file_to_upload.file.seek(0)
        UserIdentity(**current_user)
        if brain_id:
            await upload_file(
                uploadFile=file_to_upload,
                brain_id=brain_id,
                current_user=current_user,
                chat_id=None,
            )

        os.remove(new_filename)

        notification_service.update_notification_by_id(
            notification_id,
            NotificationUpdatableProperties(
                status=NotificationsStatusEnum.SUCCESS,
                description=f"Summary of {original_filename} generated successfully",
            ),
        )

        return {"message": f"{file_description} generated successfully"}
