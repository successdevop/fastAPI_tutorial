from sqlmodel.ext.asyncio.session import AsyncSession

from app.model.shipment_model import Shipment, ShipmentStatus, ShipmentEvent
from app.service.base_service import BaseService


class ShipmentEventService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(model=Shipment, session=session)

    async def add_shipment_evt(self, shipment: Shipment,
                               location: int | None = None,
                               status: ShipmentStatus | None = None,
                               description: str | None = None):

        new_shipment_evt = ShipmentEvent(
            location=location,
            status=status,
            description=description,
            shipment_id=shipment.ship_id
        )

        return await self._add(new_shipment_evt)