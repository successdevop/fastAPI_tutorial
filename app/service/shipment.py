from fastapi import HTTPException, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.model.shipment_model import Shipment
from app.schemas.shipment_schema import ShipmentUpdateSchema


class ShipmentServices:

    @staticmethod
    async def get_all_shipments(session: AsyncSession):
        sql_statement = select(Shipment)
        result = await session.exec(sql_statement)
        shipments = result.all()

        if not shipments:
            raise HTTPException(detail="No shipments record found",status_code=status.HTTP_404_NOT_FOUND)
        return shipments

    @staticmethod
    async def get_a_shipment(s_id: str, session: AsyncSession):
        sql_statement = select(Shipment).where(Shipment.ship_id == s_id)
        result = await session.exec(sql_statement)
        shipment = result.one_or_none()

        if not shipment:
            raise HTTPException(detail=f"Shipment with id {s_id} not found",status_code=status.HTTP_404_NOT_FOUND)
        return shipment

    @staticmethod
    async def delete_a_shipment(s_id: str, session: AsyncSession):
        sql_statement = select(Shipment).where(Shipment.ship_id == s_id)
        result = await session.exec(sql_statement)
        shipment = result.one_or_none()

        if not shipment:
            raise HTTPException(detail=f"Shipment with id {s_id} not found",status_code=status.HTTP_404_NOT_FOUND)

        await session.delete(shipment)
        await session.commit()
        return {"message":f"Shipment with id {s_id} deleted successfully"}

    @staticmethod
    async def update_a_shipment(s_id: str, req_body:ShipmentUpdateSchema, session: AsyncSession):
        sql_statement = select(Shipment).where(Shipment.ship_id == s_id)
        result = await session.exec(sql_statement)
        shipment = result.one_or_none()

        if not shipment:
            raise HTTPException(detail=f"Shipment with id {s_id} not found",status_code=status.HTTP_404_NOT_FOUND)

        shipment_data = req_body.model_dump(exclude_none=True)
        for k, v in shipment_data.items():
            setattr(shipment, k, v)

        session.add(shipment)
        await session.commit()
        await session.refresh(shipment)
        return shipment

        # shipment.update(shipment_data)
        # session.add(shipment)
        # await session.commit()
        # await session.refresh(shipment)
        # return shipment



