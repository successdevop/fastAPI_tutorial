from typing import List
from fastapi import APIRouter, status

from app.database.session import SessionDep
from app.schemas.shipment_schema import BaseShipmentModel, ShipmentUpdateSchema, ShipmentCreateSchema
from app.service.deliver_service import DeliveryService
from app.service.shipment_service import ShipmentServices
from app.dependency.user_dependency import SellerDep


shipment_router = APIRouter()
partner_service = DeliveryService(session=SessionDep)
shipment_service = ShipmentServices(session=SessionDep, partner_service=partner_service)

@shipment_router.get("/", response_model=List[BaseShipmentModel], status_code=status.HTTP_200_OK)
async def get_all_shipments(_: SellerDep):
    return await shipment_service.get_all_shipments()

@shipment_router.get("/{s_id}", response_model=BaseShipmentModel, status_code=status.HTTP_200_OK)
async def get_a_shipment(s_id: str):
    return await shipment_service.get_a_shipment(s_id=s_id)

@shipment_router.patch("/{s_id}", response_model=BaseShipmentModel, status_code=status.HTTP_200_OK)
async def update_a_shipment(s_id: str, req: ShipmentUpdateSchema):
    return await shipment_service.update_a_shipment(s_id=s_id, req_body=req)

@shipment_router.delete("/{s_id}", response_model=dict[str, str], status_code=status.HTTP_200_OK)
async def delete_a_shipment(s_id: str):
    return await shipment_service.delete_a_shipment(s_id=s_id)

@shipment_router.post("/", response_model=BaseShipmentModel, status_code=status.HTTP_201_CREATED)
async def create_new_shipment(seller: SellerDep, req: ShipmentCreateSchema):
    return await shipment_service.create_a_shipment(req_body=req, seller=seller)
