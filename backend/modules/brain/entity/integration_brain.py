from pydantic import BaseModel


class IntegrationBrainEntity(BaseModel):
    integration_name: str
    integration_logo_url: str
    connection_settings: dict
