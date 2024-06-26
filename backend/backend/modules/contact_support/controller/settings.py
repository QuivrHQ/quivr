from pydantic_settings import BaseSettings, SettingsConfigDict


class ContactsSettings(BaseSettings):
    model_config = SettingsConfigDict(validate_default=False)
    resend_contact_sales_from: str = "null"
    resend_contact_sales_to: str = "null"
