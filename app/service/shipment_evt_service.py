from sqlalchemy.util import ellipses_string
from sqlmodel.ext.asyncio.session import AsyncSession

from app.model.shipment_model import Shipment, ShipmentStatus, ShipmentEvent
from app.service.base_service import BaseService


class ShipmentEventService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(model=Shipment, session=session)

    async def add_shipment_evt(self, shipment: Shipment,
                               location: int | None = None,
                               description: str | None = None,
                               status: ShipmentStatus | None = None):

        if not location or not description:
            last_event = await self.get_latest_shipment(shipment)
            location = location if location is not None else last_event.location
            status = status if status is not None else last_event.status
            description = description if description is not None else self._generate_description(status, location)

        new_shipment_evt = ShipmentEvent(
            location=location,
            description=description,
            status=status,
            shipment_id=shipment.ship_id
        )

        return await self._add(new_shipment_evt)

    async def get_latest_shipment(self, shipment: Shipment):
        timeline = shipment.timeline
        timeline.sort(key=lambda item: item["created_at"])
        return timeline[-1]

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
            case _:
                return f"scanned at {location}"
