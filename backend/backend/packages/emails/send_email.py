from typing import Dict

import resend

from backend.models.settings import ResendSettings


def send_email(params: Dict):
    settings = ResendSettings()
    resend.api_key = settings.resend_api_key
    return resend.Emails.send(params)
