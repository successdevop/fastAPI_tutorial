from typing import List, Annotated
from fastapi import APIRouter, status, Request
from fastapi.params import Form
from starlette.templating import Jinja2Templates

from app.config import app_settings
from app.model.shipment_model import TagName
from app.schemas.shipment_schema import BaseShipmentModel, ShipmentUpdateSchema, ShipmentCreateSchema
from app.dependency.user_dependency import SellerDep, DeliveryPartnerDep
from app.service.service_dependency import ShipmentServiceDep
from app.util import TEMPLATE_DIR

shipment_router = APIRouter()


template = Jinja2Templates(TEMPLATE_DIR)


@shipment_router.get("/", response_model=List[BaseShipmentModel], status_code=status.HTTP_200_OK)
async def get_all_shipments(_: SellerDep, shipment_service: ShipmentServiceDep):
    return await shipment_service.get_all_shipments()


@shipment_router.patch("/{s_id}", response_model=BaseShipmentModel, status_code=status.HTTP_200_OK)
async def update_a_shipment(partner:DeliveryPartnerDep, s_id: str, req: ShipmentUpdateSchema, shipment_service: ShipmentServiceDep):
    return await shipment_service.update_a_shipment(s_id=s_id, req_body=req, partner=partner)


@shipment_router.delete("/{s_id}", response_model=dict[str, str], status_code=status.HTTP_200_OK)
async def delete_a_shipment(s_id: str, shipment_service: ShipmentServiceDep):
    return await shipment_service.delete_a_shipment(s_id=s_id)


@shipment_router.post("/", response_model=BaseShipmentModel, status_code=status.HTTP_201_CREATED)
async def create_new_shipment(seller: SellerDep, req: ShipmentCreateSchema, shipment_service: ShipmentServiceDep):
    return await shipment_service.create_a_shipment(req_body=req, seller=seller)


@shipment_router.get("/track")
async def track_shipment(request: Request, s_id: str, shipment_service: ShipmentServiceDep):
    return await shipment_service.track_shipment(s_id=s_id, request=request)


@shipment_router.get("/tag")
async def add_tag_to_shipment(s_id: str, tag_name: TagName, shipment_service: ShipmentServiceDep):
    return await shipment_service.add_tag(s_id, tag_name)


@shipment_router.get("/tag")
async def remove_tag_from_shipment(s_id: str, tag_name: TagName, shipment_service: ShipmentServiceDep):
    return await shipment_service.remove_tag(s_id, tag_name)


@shipment_router.get("/review")
async def submit_review_page(request: Request, token: str):
    return template.TemplateResponse(
        request=request,
        name="review.html",
        context={
            "review_url":f"http://{app_settings.APP_DOMAIN}/shipments/review?token={token}"
        }
    )


@shipment_router.get("/cancel/{s_id}", response_model=BaseShipmentModel, status_code=status.HTTP_200_OK)
async def cancel_shipment(s_id: str, seller: SellerDep, shipment_service: ShipmentServiceDep):
    return await shipment_service.cancel_shipment(s_id=s_id, seller=seller)


@shipment_router.get("/{s_id}", response_model=BaseShipmentModel, status_code=status.HTTP_200_OK)
async def get_a_shipment(s_id: str, shipment_service: ShipmentServiceDep):
    return await shipment_service.get_a_shipment(s_id=s_id)


@shipment_router.post("/review")
async def submit_review(token: str,
                        rating: Annotated[int | None, Form(ge=1, le=5)],
                        comment: Annotated[str | None, Form()],
                        shipment_service: ShipmentServiceDep):
    return await shipment_service.rate(token=token, rating=rating, comment=comment)

