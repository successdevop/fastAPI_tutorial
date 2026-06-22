from fastapi import BackgroundTasks
from fastapi_mail import FastMail, ConnectionConfig, MessageSchema, MessageType
from app.config import notifications_settings


class NotificationService:
    def __init__(self, task: BackgroundTasks):
        self._task = task
        self._config = ConnectionConfig(
            **notifications_settings.model_dump()
        )
        self._fastmail = FastMail(self._config)

    async def send_email_message(self, recipients: list, msg_subject: str, msg_body: str):
        print("SEND EMAIL CALLED")

        try:
            message=MessageSchema(
                recipients=recipients,
                subject=msg_subject,
                body=msg_body,
                subtype=MessageType.plain
            )

            self._task.add_task(
                self._fastmail.send_message,
                message=message
            )

            # await self._fastmail.send_message(message=message)
            print("==================================")
            print(f"Email sent to {recipients}")
            print("==================================")

        except Exception as e:
            print(f"Failed to send email: {str(e)}")
            raise e

