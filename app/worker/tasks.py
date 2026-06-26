from fastapi_mail import FastMail, ConnectionConfig, MessageSchema, MessageType
from asgiref.sync import async_to_sync
from celery import Celery

from app.config import db_settings, notifications_settings, sms_settings
from app.util import TEMPLATE_DIR


fast_mail = FastMail(
    config=ConnectionConfig(
        **notifications_settings.model_dump(),
        TEMPLATE_FOLDER=TEMPLATE_DIR
    ),
)


app = Celery(
    main="api_tasks",
    broker=db_settings.REDIS_URL(9),
    backend=db_settings.REDIS_URL(9)
)


email_sender = async_to_sync(fast_mail.send_message)


@app.task
def send_plain_email(recipients: list, msg_subject: str, msg_body: str):
    try:
        message=MessageSchema(
            recipients=recipients,
            subject=msg_subject,
            body=msg_body,
            subtype=MessageType.plain
        )

        email_sender(message=message)
        # await self._fastmail.send_message(message=message)
        print("==================================")
        print(f"Email sent to {recipients}")
        print("==================================")

    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        raise e


@app.task
def send_html_email(recipients: list, subject_msg: str, context: dict, template_name: str):
    print("SEND EMAIL CALLED")

    try:
        message=MessageSchema(
            recipients=recipients,
            subject=subject_msg,
            template_body=context,
            subtype=MessageType.html
        )

        email_sender(
            message=message,
            template_name=template_name
        )
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        raise e