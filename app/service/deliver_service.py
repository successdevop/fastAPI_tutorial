from typing import Any, Sequence

from fastapi import HTTPException, status
from sqlmodel import select, any_
from sqlmodel.ext.asyncio.session import AsyncSession
from app.database.redis_conn import add_jti_to_blacklist

from app.model.delivery_model import DeliveryPartner
from app.model.shipment_model import Shipment
from app.schemas.delivery_schema import CreateDeliverySchema, UpdateDeliverySchema
from app.service.user_service import UserService


class DeliveryService(UserService):
    def __init__(self, session: AsyncSession):
        super().__init__(DeliveryPartner, session=session)

    async def get_all_delivery_partners(self):
        result = await self.session.exec(
            select(self.model)
        )
        return result.all()

    async def register_delivery_partner(self, req_body: CreateDeliverySchema) -> DeliveryPartner:
        partner_data = req_body.model_dump()
        new_delivery_partner = await self._add_user(partner_data)
        return new_delivery_partner

    async def get_delivery_partner_by_zipcode(self, zipcode: int) -> Sequence[DeliveryPartner]:
        rsult = await self.session.exec(
            select(DeliveryPartner).where(zipcode == any_(DeliveryPartner.serviceable_zip_codes))
        )
        return rsult.all()

    async def assign_shipment(self, shipment: Shipment):
        eligible_partners = await self.get_delivery_partner_by_zipcode(shipment.destination)
        for partner in eligible_partners:
            if partner.max_handling_capacity > 0:
                partner.shipments.append(shipment)
                return partner

        raise HTTPException(
            detail="No delivery partner available",
            status_code=status.HTTP_406_NOT_ACCEPTABLE
        )

    async def update_d_partner(self, p_id: str, req_body: UpdateDeliverySchema):
        partner = await self._get(uid=p_id)
        if partner is None:
            raise HTTPException(detail=f"partner with ID ({p_id}) not found",
                                status_code=status.HTTP_404_NOT_FOUND)

        partner_data = req_body.model_dump(exclude_none=True)
        for k, v in partner_data.items():
            setattr(partner, k, v)

        return await self._update(partner)
        
    async def login_func(self, email: str, password) -> dict[str, Any]:
        token = await self._generate_token(email=email, password=password)

        return {
            "message":"Login successful",
            "access_token":token,
            "type":"jwt"
        }

    async def logout(self, token_data: dict):
        await add_jti_to_blacklist(jti=token_data["jti"])
        return {"message":"Successfully logged out"}