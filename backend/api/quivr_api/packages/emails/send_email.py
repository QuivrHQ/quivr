from typing import Dict

import resend
import smtplib
from quivr_api.models.settings import ResendSettings


def send_email(params: Dict):
    settings = ResendSettings()
    if settings.resend_api_key != "null":
        resend.api_key = settings.resend_api_key
        return resend.Emails.send(params)
    else:
        # Use SMTP to send the email
        smtp_server = settings.quivr_smtp_server
        smtp_port = settings.quivr_smtp_port
        smtp_username = settings.quivr_smtp_username
        smtp_password = settings.quivr_smtp_password

        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                if smtp_port == 587:
                    server.starttls()
                if smtp_username and smtp_password:
                    server.login(smtp_username, smtp_password)

                from_address = params.get('from', 'mail@team.quivr.app')
                to_addresses = params.get('to', [])
                subject = params.get('subject', '')
                html_content = params.get('html', '')

                message = f"From: {from_address}\n"
                message += f"To: {', '.join(to_addresses)}\n"
                message += f"Subject: {subject}\n"
                message += "Content-Type: text/html\n\n"
                message += html_content

                server.sendmail(from_address, to_addresses, message)

            return {"message": "Email sent successfully"}
        except Exception as e:
            raise Exception(f"Failed to send email: {str(e)}")
