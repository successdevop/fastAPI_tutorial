from typing import Annotated, List

from fastapi import APIRouter, status, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.delivery_schema import CreateDeliverySchema, BaseDeliverySchema, UpdateDeliverySchema
from app.database.session import SessionDep
from app.service.deliver_service import DeliveryService
from app.dependency.user_dependency import get_d_partner_access_token, DeliveryPartnerDep

delivery_router = APIRouter()
delivery_service = DeliveryService(SessionDep)


@delivery_router.post("/signup", response_model=BaseDeliverySchema, status_code=status.HTTP_201_CREATED)
async def create_deliver_partner_account(req: CreateDeliverySchema):
    return await delivery_service.register_delivery_partner(req_body=req)


@delivery_router.get("/", response_model=List[BaseDeliverySchema], status_code=status.HTTP_200_OK)
async def get_all_delivery_partner():
    return await delivery_service.get_all_delivery_partners()


@delivery_router.patch("/{p_id}", response_model=BaseDeliverySchema, status_code=status.HTTP_200_OK)
async def update_delivery_partner(_: DeliveryPartnerDep, p_id: str, req: UpdateDeliverySchema):
    return await delivery_service.update_d_partner(p_id=p_id, req_body=req)


@delivery_router.post("/login", response_model=dict, status_code=status.HTTP_200_OK)
async def login_delivery_partner(req_form: Annotated[OAuth2PasswordRequestForm, Depends()]):
    return await delivery_service.login_func(email=req_form.username, password=req_form.password)


@delivery_router.get("/logout")
async def logout_delivery_partner(token_data: Annotated[dict, Depends(get_d_partner_access_token)]):
    try:
        result = await delivery_service.logout(token_data=token_data)
        return result
    except Exception as e:
        print(f"Logout error | {e}")
        raise