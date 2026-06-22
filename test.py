import asyncio

from fastapi_mail import FastMail, ConnectionConfig, MessageSchema, MessageType
from pydantic_settings import BaseSettings


# class configuration/settings
class Notification(BaseSettings):
    MAIL_USERNAME: str = "successraphael28@gmail.com"
    MAIL_PASSWORD: str = "pltvworltgibnxns"
    MAIL_PORT: int =587
    MAIL_SERVER: str ="smtp.gmail.com"
    MAIL_FROM: str = "successraphael28@gmail.com"
    MAIL_FROM_NAME: str ="Shipment_App"
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = False

notifications = Notification()


# fastmail configuration
e_config = ConnectionConfig(
    **notifications.model_dump()
)

fastmail = FastMail(
    config=e_config
)

# async function
async def create_email_msg(recipients: list, subject_msg: str, body_msg: str):
    try:
        message = MessageSchema(
            recipients=recipients,
            subject=subject_msg,
            body=body_msg,
            subtype=MessageType.plain
        )
        await fastmail.send_message(message=message)
        print(f"Email sent to {recipients}")
    except Exception as e:
        print(f"Email not sent {str(e)}")
        raise e


# running/testing function with asyncio.run()
asyncio.run(create_email_msg(["nmesomachifaith@gmail.com"], "Is email now working",
                             "If email is working say HI otherwise say NAY"))