from typing import Annotated, List

from fastapi import APIRouter, status, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.seller_shema import CreateSellerSchema, BaseSellerSchema
from app.dependency.user_dependency import get_seller_access_token
from app.service.service_dependency import SellerServiceDep


seller_router = APIRouter()

@seller_router.post("/signup", response_model=BaseSellerSchema, status_code=status.HTTP_201_CREATED)
async def create_seller_account(req: CreateSellerSchema, seller_service: SellerServiceDep):
    return await seller_service.register_seller(req_body=req)


@seller_router.get("/", response_model=List[BaseSellerSchema], status_code=status.HTTP_200_OK)
async def get_all_sellers(seller_service: SellerServiceDep):
    return await seller_service.get_all_sellers()


@seller_router.get("/verify")
async def verify_seller_mail(token: str, service: SellerServiceDep):
    await service.verify_email(token=token)
    return {"detail":"Account verified"}


# Login user
@seller_router.post("/login", response_model=dict, status_code=status.HTTP_200_OK)
async def login_seller(req_form: Annotated[OAuth2PasswordRequestForm, Depends()], seller_service: SellerServiceDep):
    return await seller_service.login_func(email=req_form.username, password=req_form.password)


@seller_router.get("/logout")
async def logout_seller(token_data: Annotated[dict, Depends(get_seller_access_token)], seller_service: SellerServiceDep):
    try:
        result = await seller_service.logout(token_data=token_data)
        return result
    except Exception as e:
        print(f"Logout error | {e}")
        raise

@seller_router.delete("/delete/{s_id}")
async def delete_seller(s_id: str, seller_service: SellerServiceDep):
    await seller_service.delete_seller(s_id=s_id)
    return {"details":"deleted successfully"}
