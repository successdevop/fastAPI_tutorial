from fastapi import HTTPException, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.model.seller_model import Seller
from app.model.shipment_model import Shipment
from app.schemas.shipment_schema import ShipmentUpdateSchema, ShipmentCreateSchema
from app.service.base_service import BaseService


class ShipmentServices(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(Shipment, session=session)

    async def get_all_shipments(self):
        sql_statement = select(self.model)
        result = await self.session.exec(sql_statement)
        shipments = result.all()

        if not shipments:
            raise HTTPException(detail="No shipments record found",status_code=status.HTTP_404_NOT_FOUND)
        return shipments

    async def get_a_shipment(self, s_id: str):
        shipment = await self._get(uid=s_id)
        if not shipment:
            raise HTTPException(detail=f"Shipment with id {s_id} not found",status_code=status.HTTP_404_NOT_FOUND)
        return shipment

    async def delete_a_shipment(self, s_id: str):
        shipment = await self._get(uid=s_id)
        if not shipment:
            raise HTTPException(detail=f"Shipment with id {s_id} not found",status_code=status.HTTP_404_NOT_FOUND)

        await self._delete(shipment)
        return {"message":f"Shipment with id {s_id} deleted successfully"}

    async def update_a_shipment(self, s_id: str, req_body:ShipmentUpdateSchema):
        shipment = await self._get(uid=s_id)
        if not shipment:
            raise HTTPException(detail=f"Shipment with id {s_id} not found",status_code=status.HTTP_404_NOT_FOUND)

        shipment_data = req_body.model_dump(exclude_none=True)
        for k, v in shipment_data.items():
            setattr(shipment, k, v)

        await self._update(shipment)

        # shipment.update(shipment_data)
        # session.add(shipment)
        # await session.commit()
        # await session.refresh(shipment)
        # return shipment

    async def create_a_shipment(self, req_body: ShipmentCreateSchema, seller: Seller):
        shipment_data = req_body.model_dump()
        new_shipment = Shipment(**shipment_data, seller_id=seller.seller_id)

        await self._add(new_shipment)



