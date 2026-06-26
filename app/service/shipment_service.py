from fastapi import HTTPException, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette.templating import Jinja2Templates

from app.auth.auth_utils import decode_url_safe_token
from app.database.redis_conn import get_shipment_verification_code
from app.dependency.user_dependency import DeliveryPartnerDep, SellerDep
from app.model.seller_model import Seller
from app.model.shipment_model import Shipment, ShipmentStatus, ShipmentsReview
from app.schemas.shipment_schema import ShipmentUpdateSchema, ShipmentCreateSchema
from app.service.base_service import BaseService
from app.service.deliver_service import DeliveryPartnerService
from app.service.shipment_evt_service import ShipmentEventService
from app.util import TEMPLATE_DIR


template = Jinja2Templates(TEMPLATE_DIR)


class ShipmentServices(BaseService):
    def __init__(self, session: AsyncSession, partner_service: DeliveryPartnerService,
                 event_service: ShipmentEventService):
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

        if req_body.status == ShipmentStatus.DELIVERED:
            code = await get_shipment_verification_code(s_id)

            if code != req_body.verification_code:
                raise HTTPException(detail="Client not authorized", status_code=status.HTTP_401_UNAUTHORIZED)

        shipment_data = req_body.model_dump(exclude_none=True, exclude=["verification_code"])
        if not shipment_data:
            raise HTTPException(detail="No data provided for update", status_code=status.HTTP_400_BAD_REQUEST)

        await self.event_service.add_shipment_evt(
            shipment=shipment,
            **shipment_data
        )

        return await self._update(shipment)

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

    async def cancel_shipment(self, s_id: str, seller:SellerDep):
        shipment = await self._get(uid=s_id)
        if not shipment:
            raise HTTPException(detail=f"Shipment with id {s_id} not found", status_code=status.HTTP_404_NOT_FOUND)

        if shipment.seller_id != seller.id:
            raise HTTPException(detail="Not authorized", status_code=status.HTTP_401_UNAUTHORIZED)

        event = await self.event_service.add_shipment_evt(
            shipment=shipment,
            status=ShipmentStatus.CANCELLED
        )

        shipment.timeline.append(event)

        return shipment

    async def track_shipment(self, request, s_id: str):
        shipment = await self._get(uid=s_id)
        if not shipment:
            raise HTTPException(detail=f"Shipment with id {s_id} not found", status_code=status.HTTP_404_NOT_FOUND)

        # if seller.id != shipment.seller_id:
        #     raise HTTPException(detail="Not authorized", status_code=status.HTTP_401_UNAUTHORIZED)

        context = shipment.model_dump()
        context["partner"] = shipment.delivery.user_name
        context["status"] = shipment.status
        context["timeline"] = shipment.timeline

        return template.TemplateResponse(
            request=request,
            name="track_shipment.html",
            context=context
        )

    async def rate(self, token: str, rating: int | None, comment: str | None):
        token_data = decode_url_safe_token(token=token)

        if not token_data:
            raise HTTPException(detail="Invalid token", status_code=status.HTTP_400_BAD_REQUEST)

        shipment = await self._get(uid=token_data["id"])

        new_review = ShipmentsReview(
            rating=rating,
            comment=comment,
            shipment_id=shipment.ship_id
        )

        await self._add(new_review)
        return {"details":"Review submitted"}







