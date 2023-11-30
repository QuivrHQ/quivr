from pydantic import BaseSettings


class ContactsSettings(BaseSettings):
    resend_contact_sales_from: str = "null"
    resend_contact_sales_to: str = "null"
