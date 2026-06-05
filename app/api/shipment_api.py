from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.database.session import SessionDep
from app.service.shipment import ShipmentServices


shipment_router = APIRouter()

session: AsyncSession = Depends(SessionDep)
shipment_service = ShipmentServices(session=session)

@shipment_router.get("/")
async def get_all_shipments():
    return await shipment_service.get_all_shipments()