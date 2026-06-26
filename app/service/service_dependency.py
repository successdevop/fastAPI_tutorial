from typing import Annotated

from fastapi import Depends, BackgroundTasks

from app.database.session import SessionDep
from app.service.deliver_service import DeliveryPartnerService
from app.service.seller_service import SellerService
from app.service.shipment_evt_service import ShipmentEventService
from app.service.shipment_service import ShipmentServices


def get_delivery_service(session: SessionDep):
    return DeliveryPartnerService(session=session)


def get_shipment_service(session: SessionDep, task: BackgroundTasks):
    return ShipmentServices(
        session=session,
        partner_service=DeliveryPartnerService(session=session),
        event_service=ShipmentEventService(session=session, task=task)
    )


def get_seller_service(session: SessionDep):
    return SellerService(session=session)


def get_event_service(session: SessionDep, task: BackgroundTasks):
    return ShipmentEventService(session=session, task=task)


DeliveryServiceDep = Annotated[DeliveryPartnerService, Depends(get_delivery_service)]
ShipmentServiceDep = Annotated[ShipmentServices, Depends(get_shipment_service)]
SellerServiceDep = Annotated[SellerService, Depends(get_seller_service)]