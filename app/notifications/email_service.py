from fastapi_mail import FastMail, ConnectionConfig, MessageSchema, MessageType
from app.config import notifications_settings


class NotificationService:
    def __init__(self):
        self.fastmail = FastMail(
            ConnectionConfig(
                **notifications_settings.model_dump()
            )
        )

    async def send_email_message(self, recipients: list, msg_subject: str, msg_body: str):
        await self.fastmail.send_message(
            message=MessageSchema(
                recipients=recipients,
                subject=msg_subject,
                body=msg_body,
                subtype=MessageType.plain
            )
        )
        print("Email sent")
