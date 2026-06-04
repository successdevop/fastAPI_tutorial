from sqlmodel.ext.asyncio.session import AsyncSession
from app.model.shipment_model import Shipment


class ShipmentServices:
    async def get_all_shipments(self, session: AsyncSession):
        pass