# Extract and combine content recursively
from typing import Dict, Optional, Type

from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain.pydantic_v1 import BaseModel as BaseModelV1
from langchain.pydantic_v1 import Field as FieldV1
from langchain_community.document_loaders import PlaywrightURLLoader
from langchain_core.tools import BaseTool
from pydantic import BaseModel
from quivr_api.logger import get_logger
from quivr_api.models.settings import BrainSettings
from quivr_api.modules.contact_support.controller.settings import ContactsSettings
from quivr_api.packages.emails.send_email import send_email

logger = get_logger(__name__)


class EmailInput(BaseModelV1):
    text: str = FieldV1(
        ...,
        title="text",
        description="text to send in HTML email format. Use pretty formating, use bold, italic, next line, etc...",
    )


class EmailSenderTool(BaseTool):
    user_email: str
    name = "email-sender"
    description = "useful for when you need to send an email."
    args_schema: Type[BaseModel] = EmailInput
    brain_settings: BrainSettings = BrainSettings()
    contact_settings: ContactsSettings = ContactsSettings()

    def _run(
        self, text: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> Dict:
        html_body = """
        <div style="text-align: center;">
                <img src="https://quivr-cms.s3.eu-west-3.amazonaws.com/logo_quivr_white_7e3c72620f.png" alt="Quivr Logo" style="width: 100px; height: 100px; border-radius: 50%; margin: 0 auto; display: block;">
                <br />
            </div>
            """
        html_body += f"""
            {text}
            """
        logger.debug(f"Email body: {html_body}")
        logger.debug(f"Email to: {self.user_email}")
        logger.debug(f"Email from: {self.contact_settings.resend_contact_sales_from}")
        try:
            r = send_email(
                {
                    "from": self.contact_settings.resend_contact_sales_from,
                    "to": self.user_email,
                    "reply_to": "no-reply@quivr.app",
                    "subject": "Email from your assistant",
                    "html": html_body,
                }
            )
            logger.info("Resend response", r)
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            return {"content": "Error sending email because of error: " + str(e)}

        return {"content": "Email sent"}

    async def _arun(
        self, url: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> Dict:
        """Run the tool asynchronously."""
        loader = PlaywrightURLLoader(urls=[url], remove_selectors=["header", "footer"])
        data = loader.load()

        extracted_content = ""
        for page in data:
            extracted_content += page.page_content

        return {"content": extracted_content}
