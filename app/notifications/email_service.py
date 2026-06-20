import asyncio

from fastapi_mail import FastMail, ConnectionConfig, MessageSchema, MessageType
from app.config import notifications_settings


fastmail = FastMail(
    ConnectionConfig(
        **notifications_settings.model_dump()
    )
)

async def send_message():
    await fastmail.send_message(
        message=MessageSchema(
            recipients=["nmesomachifaith@gmail.com"],
            subject="First email with python",
            body="This is a shipment application",
            subtype=MessageType.plain
        )
    )
    print("Email sent")

asyncio.run(send_message())