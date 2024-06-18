import smtplib
from email.message import EmailMessage
from typing import Sequence


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
    except Exception as e:  # noqa # pylint: disable=broad-except
        return False
    return True
