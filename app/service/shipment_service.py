from fastapi import HTTPException, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.dependency.user_dependency import DeliveryPartnerDep
from app.model.seller_model import Seller
from app.model.shipment_model import Shipment
from app.schemas.shipment_schema import ShipmentUpdateSchema, ShipmentCreateSchema
from app.service.base_service import BaseService
from app.service.deliver_service import DeliveryPartnerService
from app.service.shipment_evt_service import ShipmentEventService


class ShipmentServices(BaseService):
    def __init__(self, session: AsyncSession, partner_service: DeliveryPartnerService, event_service: ShipmentEventService):
        super().__init__(model=Shipment, session=session)
        self.partner_service = partner_service
        self.event_service = event_service

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

    async def update_a_shipment(self, s_id: str, req_body:ShipmentUpdateSchema, partner: DeliveryPartnerDep):
        shipment = await self._get(uid=s_id)
        if not shipment:
            raise HTTPException(detail=f"Shipment with id {s_id} not found",status_code=status.HTTP_404_NOT_FOUND)

        if shipment.del_partner_id != partner.id:
            raise HTTPException(detail="Not authorized", status_code=status.HTTP_401_UNAUTHORIZED)

        if not req_body:
            raise HTTPException(detail="No data provided for update", status_code=status.HTTP_400_BAD_REQUEST)

        shipment_data = req_body.model_dump(exclude_none=True)
        for k, v in shipment_data.items():
            setattr(shipment, k, v)

        await self._update(shipment)

    async def create_a_shipment(self, req_body: ShipmentCreateSchema, seller: Seller):
        shipment_data = req_body.model_dump()

        new_shipment = Shipment(**shipment_data, seller_id=seller.id)
        partner = await self.partner_service.assign_shipment(new_shipment)
        new_shipment.del_partner_id = partner.id

        shipment = await self._add(new_shipment)

        event = await self.event_service.add_shipment_evt(
            shipment=shipment,
            location=seller.zip_code,
            description=f"assigned to {partner.user_name}"
        )

        shipment.timeline.append(event)

        return shipment



