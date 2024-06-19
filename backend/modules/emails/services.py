from datetime import datetime
from typing import Sequence

from django.utils.translation import gettext as _

from config import settings
from modules.apartments.models import Apartment
from modules.emails.body_templates import get_message_template
from modules.emails.utils import create_html_message, create_message, send_email


class EmailService:
    DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
    LOGIN = settings.EMAIL_USER
    PASSWORD = settings.EMAIL_APP_CLIENT_ACCESS_CODE

    def _send_email_to(
        self, receiver: str | Sequence[str], subject: str, body: str
    ) -> bool:
        message = create_html_message(self.LOGIN, receiver, subject, body)
        return send_email(message, self.LOGIN, self.PASSWORD, receiver)

    def send_offers(
        self,
        receiver: str | Sequence[str],
        offers: list[Apartment],
    ) -> bool:
        title = _("New cool apartments offers: ") + datetime.now().strftime(
            self.DATE_FORMAT
        )
        message = get_message_template(offers)
        return self._send_email_to(receiver, title, message)
