from fastapi import APIRouter
from pydantic import BaseModel
from quivr_api.logger import get_logger
from quivr_api.modules.contact_support.controller.settings import ContactsSettings
from quivr_api.packages.emails.send_email import send_email


class ContactMessage(BaseModel):
    customer_email: str
    content: str


contact_router = APIRouter()
logger = get_logger(__name__)


def resend_contact_sales_email(customer_email: str, content: str):
    settings = ContactsSettings()
    mail_from = settings.resend_contact_sales_from
    mail_to = settings.resend_contact_sales_to
    body = f"""
    <p>Customer email: {customer_email}</p>
    <p>{content}</p>
    """
    params = {
        "from": mail_from,
        "to": mail_to,
        "subject": "Contact sales",
        "reply_to": customer_email,
        "html": body,
    }

    return send_email(params)


@contact_router.post("/contact")
def post_contact(message: ContactMessage):
    try:
        resend_contact_sales_email(message.customer_email, message.content)
    except Exception as e:
        logger.error(e)
        return {"error": "There was an error sending the email"}
