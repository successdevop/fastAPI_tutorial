from typing import Annotated

from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.auth.auth_utils import decode_token
from app.schemas.seller_shema import CreateSellerSchema, BaseSellerSchema
from app.database.session import SessionDep
from app.security.security import oauth2_scheme
from app.service.seller_service import SellerService

seller_router = APIRouter()
seller_service = SellerService()

@seller_router.post("/signup", response_model=BaseSellerSchema, status_code=status.HTTP_201_CREATED)
async def create_seller_account(req: CreateSellerSchema, session: SessionDep):
    return await seller_service.register_seller(req_body=req, session=session)

# Login user
@seller_router.post("/login", response_model=dict, status_code=status.HTTP_200_OK)
async def login_seller(req_form: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep):
    print("was here")
    return await seller_service.login_func(email=req_form.username, password=req_form.password, session=session)


@seller_router.get("/dashboard")
async def get_dashboard(token: str = Depends(oauth2_scheme)):
    result = decode_token(token=token)
    if result is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid access token")
    return {"message":"successfully authenticated"}