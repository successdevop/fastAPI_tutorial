from typing import Annotated

from fastapi import Depends

from app.database.session import SessionDep
from app.service.deliver_service import DeliveryPartnerService
from app.service.seller_service import SellerService
from app.service.shipment_service import ShipmentServices


def get_delivery_service(session: SessionDep):
    return DeliveryPartnerService(session=session)


def get_shipment_service(session: SessionDep):
    return ShipmentServices(
        session=session,
        partner_service=DeliveryPartnerService(session=session)
    )


def get_seller_service(session: SessionDep):
    return SellerService(session=session)


DeliveryServiceDep = Annotated[DeliveryPartnerService, Depends(get_delivery_service)]
ShipmentServiceDep = Annotated[ShipmentServices, Depends(get_shipment_service)]
SellerServiceDep = Annotated[SellerService, Depends(get_seller_service)]