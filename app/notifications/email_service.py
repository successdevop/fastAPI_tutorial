from fastapi import BackgroundTasks
from fastapi_mail import FastMail, ConnectionConfig, MessageSchema, MessageType
from app.config import notifications_settings
from app.util import TEMPLATE_DIR


class NotificationService:
    def __init__(self, task: BackgroundTasks):
        self._task = task
        self._config = ConnectionConfig(
            **notifications_settings.model_dump(),
            TEMPLATE_FOLDER=TEMPLATE_DIR
        )
        self._fastmail = FastMail(self._config)

    def send_email_message(self, recipients: list, msg_subject: str, msg_body: str):
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

    def send_email_message_with_html(self, recipients: list, subject_msg: str, context: dict, template_name: str):
        print("SEND EMAIL CALLED")

        try:
            message=MessageSchema(
                recipients=recipients,
                subject=subject_msg,
                template_body=context,
                subtype=MessageType.html
            )

            self._task.add_task(
                self._fastmail.send_message,
                message=message,
                template_name=template_name
            )

        except Exception as e:
            print(f"Failed to send email: {str(e)}")
            raise e

