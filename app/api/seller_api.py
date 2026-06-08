from typing import Annotated

from fastapi import APIRouter, status, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.seller_shema import CreateSellerSchema, BaseSellerSchema
from app.database.session import SessionDep
from app.service.seller_service import SellerService


seller_router = APIRouter()
seller_service = SellerService()


@seller_router.post("/signup", response_model=BaseSellerSchema, status_code=status.HTTP_201_CREATED)
async def create_seller_account(req: CreateSellerSchema, session: SessionDep):
    return await seller_service.register_seller(req_body=req, session=session)


# Login user
@seller_router.post("/login", response_model=dict, status_code=status.HTTP_200_OK)
async def login_seller(req_form: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep):
    return await seller_service.login_func(email=req_form.username, password=req_form.password, session=session)

@seller_router.get("/logout")
async def logout_seller(token_data: Annotated[dict, Depends(get_access_token)]):
    return await seller_service.logout(token_data=token_data)