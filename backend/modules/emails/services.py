import smtplib
from datetime import datetime
from email.message import EmailMessage
from typing import Sequence

from modules.apartments.models import ApartmentDetails, Apartment
from django.utils.translation import gettext as _

from modules.emails.email_body_templates import get_message_template
from backend.config import settings as config


def create_message(from_: str, to: str | Sequence[str], subject: str, body: str) -> EmailMessage:
    message = EmailMessage()
    message['From'] = from_
    message['To'] = to
    message['Subject'] = subject
    message.set_content(body)
    return message


def send_email(
    message: EmailMessage, login: str, password: str, receiver: str | Sequence[str]
) -> bool:
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(login, password)
            smtp.sendmail(login, receiver, message.as_string())
    except Exception as e:  # TODO: Add logging
        return False
    return True


class EmailService:
    DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

    def __init__(self):
        self.login = config.EMAIL_USER
        self.password = config.EMAIL_APP_CLIENT_ACCESS_CODE

    def _send_email_to(self, receiver: str, subject: str, body: str) -> bool:
        message = create_message(self.login, self.login, subject, body)
        return send_email(message, self.login, self.password, receiver)

    def send_offers(self, receiver: str, offers: list[tuple[Apartment, ApartmentDetails]]) -> bool:
        title = _("New cool apartments offers: ") + datetime.now().strftime(self.DATE_FORMAT)
        message = get_message_template(offers)
        return self._send_email_to(receiver, title, message)
