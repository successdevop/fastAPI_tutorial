# import asyncio
#
# from fastapi_mail import FastMail, ConnectionConfig, MessageSchema, MessageType
# from pydantic_settings import BaseSettings
#
#
# # class configuration/settings
# class Notification(BaseSettings):
#     MAIL_USERNAME: str = "successraphael28@gmail.com"
#     MAIL_PASSWORD: str = "pltvworltgibnxns"
#     MAIL_PORT: int =587
#     MAIL_SERVER: str ="smtp.gmail.com"
#     MAIL_FROM: str = "successraphael28@gmail.com"
#     MAIL_FROM_NAME: str ="Shipment_App"
#     MAIL_STARTTLS: bool = True
#     MAIL_SSL_TLS: bool = False
#     USE_CREDENTIALS: bool = True
#     VALIDATE_CERTS: bool = False
#
# notifications = Notification()
#
#
# # fastmail configuration
# e_config = ConnectionConfig(
#     **notifications.model_dump()
# )
#
# fastmail = FastMail(
#     config=e_config
# )
#
# # async function
# async def create_email_msg(recipients: list, subject_msg: str, body_msg: str):
#     try:
#         message = MessageSchema(
#             recipients=recipients,
#             subject=subject_msg,
#             body=body_msg,
#             subtype=MessageType.plain
#         )
#         await fastmail.send_message(message=message)
#         print(f"Email sent to {recipients}")
#     except Exception as e:
#         print(f"Email not sent {str(e)}")
#         raise e
#
#
# # running/testing function with asyncio.run()
# asyncio.run(create_email_msg(["nmesomachifaith@gmail.com"], "Is email now working",
#                              "If email is working say HI otherwise say NAY"))


# import asyncio
# import httpx
#
# async def main():
#     async with httpx.AsyncClient() as client:
#         r = await client.get("https://api.pingram.io")
#         print(r.status_code)
#
# asyncio.run(main())

# import asyncio
# from pingram import Pingram
#
# API_KEY = "your_actual_key"
#
#
# async def main():
#     try:
#         async with Pingram(
#                 API_KEY,
#                 base_url="https://api.pingram.io"
#         ) as client:
#             print("Client created successfully")
#     except Exception as e:
#         print(type(e))
#         print(e)
#
#
# asyncio.run(main())



import asyncio
import logging

from pingram import Pingram

import httpx

httpx_logger = logging.getLogger("httpx")
httpx_logger.setLevel(logging.DEBUG)
httpx_logger.addHandler(logging.StreamHandler())

API_KEY = "pingram_sk_eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiJrZXlfZGQwYzczNjkzZDJiZjIyZGFiNDUwNjVjODExZTFiOWYiLCJ2ZXJzaW9uIjoxLCJhY2NvdW50SWQiOiI4aTlvZ20zZWs0aWFxbnhjZmVtaHJ3Njg5eiIsImtleVR5cGUiOiJzZWNyZXQiLCJlbnZpcm9ubWVudElkIjoiOGk5b2dtM2VrNGlhcW54Y2ZlbWhydzY4OXoifQ.D5mhOFPq_cWzIHbNqTvG0aSlp9sA1Ah9B7nblFO-g8Y"

payload = {
    "type": "sms_compose_preview",
    "to": {
        "number": "+2348139111114"
    },
    "sms": {
        "message": "Test message"
    }
}


async def main():
    try:
        async with Pingram(
                API_KEY,
                base_url="https://api.pingram.io"
        ) as client:
            response = await client.send(payload)
            print(response)

    except Exception as e:
        print(type(e))
        print(e)


asyncio.run(main())