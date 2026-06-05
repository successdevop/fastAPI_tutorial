from typing import List

from fastapi import APIRouter, status

from app.database.session import SessionDep
from app.schemas.shipment_schema import BaseShipmentModel
from app.service.shipment import ShipmentServices


shipment_router = APIRouter()
shipment_service = ShipmentServices()

@shipment_router.get("/", response_model=List[BaseShipmentModel], status_code=status.HTTP_200_OK)
async def get_all_shipments(session: SessionDep):
    return await shipment_service.get_all_shipments(session=session)
