import traceback

from fastapi import BackgroundTasks, HTTPException
from pingram import Pingram

from app.config import sms_settings


class SMSService:
    def __init__(self, task: BackgroundTasks):
        self._task = task

    async def _send_sms(self, recipient_number: str, message: str):
        try:
            # Prepare notification payload
            notification_payload = {
                "type": "sms_compose_preview",
                "to": {
                    "number": recipient_number
                },
                "sms": {
                    "message": message
                }
            }

            if not sms_settings.PINGRAM_API_KEY:
                raise ValueError("PINGRAM_API_KEY is not configured")

            # Send notification using async context manager
            async with Pingram(sms_settings.PINGRAM_API_KEY, base_url="https://api.pingram.io") as client:
                response = await client.send(notification_payload)

            return {
                "success": True,
                "message": "Notification sent successfully",
                "response": response
            }
        except Exception as e:
            print("=" * 80)
            print(f"failed to send SMS to {recipient_number} || {e}")
            print(type(e))
            print(repr(e))
            traceback.print_exc()
            print("=" * 80)

    def send_sms_notification(self, recipient_number: str, message: str):
        if not recipient_number:
            raise ValueError("Recipient number is required")

        if not message.strip():
            raise ValueError("Message cannot be empty")
        
        self._task.add_task(
            self._send_sms,
            recipient_number=recipient_number,
            message=message
        )