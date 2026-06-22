from fastapi_mail import FastMail, ConnectionConfig, MessageSchema, MessageType
from app.config import notifications_settings


class NotificationService:
    def __init__(self):
        self._config = ConnectionConfig(
            **notifications_settings.model_dump()
        )
        self._fastmail = FastMail(self._config)

    async def send_email_message(self, recipients: list, msg_subject: str, msg_body: str):
        try:
            message=MessageSchema(
                recipients=recipients,
                subject=msg_subject,
                body=msg_body,
                subtype=MessageType.plain
            )

            await self._fastmail.send_message(message=message)
            print(f"Email sent to {recipients}")
        except Exception as e:
            print(f"Failed to send email: {str(e)}")
            raise e

