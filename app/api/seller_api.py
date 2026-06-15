from typing import Annotated, List

from fastapi import APIRouter, status, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.seller_shema import CreateSellerSchema, BaseSellerSchema
from app.database.session import SessionDep
from app.service.seller_service import SellerService
from app.dependency.user_dependency import get_seller_access_token


seller_router = APIRouter()
seller_service = SellerService(session=SessionDep)


@seller_router.post("/signup", response_model=BaseSellerSchema, status_code=status.HTTP_201_CREATED)
async def create_seller_account(req: CreateSellerSchema):
    return await seller_service.register_seller(req_body=req)


@seller_router.get("/", response_model=List[BaseSellerSchema], status_code=status.HTTP_200_OK)
async def get_all_sellers():
    return await seller_service.get_all_sellers()


# Login user
@seller_router.post("/login", response_model=dict, status_code=status.HTTP_200_OK)
async def login_seller(req_form: Annotated[OAuth2PasswordRequestForm, Depends()]):
    return await seller_service.login_func(email=req_form.username, password=req_form.password)


@seller_router.get("/logout")
async def logout_seller(token_data: Annotated[dict, Depends(get_seller_access_token)]):
    try:
        result = await seller_service.logout(token_data=token_data)
        return result
    except Exception as e:
        print(f"Logout error | {e}")
        raise