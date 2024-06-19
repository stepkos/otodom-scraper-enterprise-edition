import smtplib
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Sequence


def create_message(
        from_: str, to: str | Sequence[str], subject: str, body: str
) -> EmailMessage:
    message = EmailMessage()
    message["From"] = from_
    message["To"] = to
    message["Subject"] = subject
    message.set_content(body)
    return message


def create_html_message(
        from_: str, to: str | Sequence[str], subject: str, html_str: str
) -> MIMEMultipart:
    message = MIMEMultipart("alternative")
    message["From"] = from_
    message["To"] = to
    message["Subject"] = subject
    message.attach(MIMEText("HELLO HELLO", "plain"))
    message.attach(MIMEText(html_str, "html"))
    return message


def send_email(
        message: EmailMessage | MIMEMultipart, login: str, password: str, receiver: str | Sequence[str]
) -> bool:
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(login, password)
            smtp.sendmail(login, receiver, message.as_string())
    except Exception as e:  # noqa # pylint: disable=broad-except
        return False
    return True
