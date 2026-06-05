from fastapi import HTTPException, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.model.shipment_model import Shipment


class ShipmentServices:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_shipments(self):
        sql_statements = select(Shipment)
        shipments = await self.session.exec(sql_statements)
        result = shipments.all()

        if not result:
            raise HTTPException(
                detail="No shipments found",
                status_code=status.HTTP_404_NOT_FOUND
            )

        return result