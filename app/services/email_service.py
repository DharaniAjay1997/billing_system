import smtplib

from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.core.config import settings


class EmailService:

    @classmethod
    def send_email(
        cls,
        recipient: str,
        subject: str,
        body: str,
        attachment_path: str | None = None,
    ):

        message = MIMEMultipart()

        message["From"] = settings.smtp_username or "no-reply@example.com"
        message["To"] = recipient
        message["Subject"] = subject

        message.attach(
            MIMEText(body, "plain")
        )

        if attachment_path:

            with open(
                attachment_path,
                "rb",
            ) as file:

                attachment = MIMEApplication(
                    file.read(),
                    Name=attachment_path.split("/")[-1],
                )

            attachment["Content-Disposition"] = (
                f'attachment; filename="{attachment_path.split("/")[-1]}"'
            )

            message.attach(
                attachment
            )

        with smtplib.SMTP(
            settings.smtp_server,
            settings.smtp_port,
        ) as smtp:

            smtp.ehlo()

            # Authenticate only if credentials are configured
            if (
                settings.smtp_username
                and settings.smtp_password
            ):
                smtp.starttls()
                smtp.ehlo()

                smtp.login(
                    settings.smtp_username,
                    settings.smtp_password,
                )

            smtp.send_message(message)