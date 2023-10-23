from fastapi import APIRouter
import resend
from logger import get_logger
from models import ContactsSettings
from pydantic import BaseModel

class ContactMessage(BaseModel):
    customer_email: str
    content: str

router = APIRouter()
logger = get_logger(__name__)

def resend_contact_sales_email(customer_email: str, content: str):
    settings = ContactsSettings()
    resend.api_key = settings.resend_api_key
    mail_from = settings.resend_contact_sales_from
    mail_to = settings.resend_contact_sales_to
    params = {
        "from": f"Customer <{mail_from}>",
        "to": mail_to,
        "subject": "Contact sales",
        "reply_to": customer_email,
        "html": f"<p>{content}</p>",
    }
    logger.info(params)
    resend.Emails.send(params)

@router.post("/contact")
def post_contact(message: ContactMessage):
    try:
        resend_contact_sales_email(message.customer_email, message.content)
    except Exception as e:
        logger.error(e)
        return {"error": "There was an error sending the email"}
