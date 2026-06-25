from datetime import datetime
from operator import attrgetter
from random import randint

from sqlmodel.ext.asyncio.session import AsyncSession

from app.database.redis_conn import add_shipment_verification_code
from app.model.shipment_model import Shipment, ShipmentStatus, ShipmentEvent
from app.notifications.email_service import NotificationService
from app.notifications.sms_service import SMSService
from app.service.base_service import BaseService


class ShipmentEventService(BaseService):
    def __init__(self, session: AsyncSession, task):
        super().__init__(model=ShipmentEvent, session=session)
        self.notification_service = NotificationService(task=task)
        self.sms_service = SMSService(task=task)

    async def add_shipment_evt(self, shipment: Shipment,
                               location: int | None = None,
                               description: str | None = None,
                               status: ShipmentStatus = ShipmentStatus.PLACED):

        last_event = await self.get_latest_shipment(shipment)
        if last_event:
            location = location if location is not None else last_event.location
            status = status if status is not None else last_event.status
            description = description if description is not None else self._generate_description(status, location)

        new_shipment_evt = ShipmentEvent(
            location=location,
            description=description,
            status=status,
            shipment_id=shipment.ship_id
        )

        await self._notify(shipment=shipment, status=status)

        return await self._add(new_shipment_evt)

    async def get_latest_shipment(self, shipment: Shipment):
        if not shipment.timeline:
            return None

        return max(shipment.timeline, key=attrgetter("created_at"))

    def _generate_description(self, status: ShipmentStatus, location: int):
        match status:
            case ShipmentStatus.PLACED:
                return "assigned delivery partner"
            case ShipmentStatus.IN_TRANSIT:
                return "shipment in transit"
            case ShipmentStatus.DELIVERED:
                return "shipment successfully delivered"
            case ShipmentStatus.OUT_OF_DELIVERY:
                return "shipment out of delivery"
            case ShipmentStatus.CANCELLED:
                return "shipment cancelled by seller"
            case _:
                return f"scanned at {location}"

    async def _notify(self, shipment: Shipment, status: ShipmentStatus):
        print("NOTIFY called")
        print(status)
        print("=======================")
        print(shipment.seller.user_name)
        print(shipment.delivery.user_name)
        print("==========================")

        match status:
            case status.PLACED:
                await self.notification_service.send_email_message_with_html(
                    recipients=[shipment.client_contact_email],
                    subject_msg="Your order is being processed",
                    context={
                        "seller": shipment.seller.user_name,
                        "ship_id": shipment.ship_id,
                        "content": shipment.content,
                        "weight": shipment.weight,
                        "created": datetime.strftime(shipment.created_at, "%Y-%m-%d %H:%M:%S"),
                        "status": status.value.lower(),
                        "client_email": shipment.client_contact_email
                    },
                    template_name="mail_placed.html"
                )
                # await self.notification_service.send_email_message(
                #     recipients=[shipment.client_contact_email],
                #     msg_subject="Your Order is shipped",
                #     msg_body=f"Your order with {shipment.seller.user_name} is picked up by {shipment.delivery.user_name}"
                #              f" and is on it's way to you"
                # )

            case ShipmentStatus.IN_TRANSIT:
                await self.notification_service.send_email_message(
                    recipients=[shipment.client_contact_email],
                    msg_subject="Your order is shipped",
                    msg_body=f"Your order with {shipment.seller.user_name} is on transit with {shipment.delivery.user_name}"
                             f" and is on it's way to you"
                )

                code = randint(100_000, 999_999)
                await add_shipment_verification_code(shipment.ship_id, code)

                if shipment.client_contact_phone:
                    self.sms_service.send_sms_notification(
                        recipient_number=shipment.client_contact_phone,
                        message=f"Your order is arriving soon! Share the code ({code}) with the delivery executive to "
                                f"receive your package"
                    )

            case ShipmentStatus.OUT_OF_DELIVERY:
                await self.notification_service.send_email_message(
                    recipients=[shipment.client_contact_email],
                    msg_subject="Your order is on queue",
                    msg_body=f"shipment is currently out of stock"
                )

            case ShipmentStatus.DELIVERED:
                await self.notification_service.send_email_message(
                    recipients=[shipment.client_contact_email],
                    msg_subject="Your order is Delivered",
                    msg_body=f"Your order with {shipment.delivery.user_name} has been delivered"
                )

