from fastapi import APIRouter, status

from app.schemas.BaseSellerModel import CreateSellerSchema, BaseSellerSchema
from app.database.session import SessionDep
from app.service.seller_service import SellerService

seller_router = APIRouter()
seller_service = SellerService()

@seller_router.post("/", response_model=BaseSellerSchema, status_code=status.HTTP_201_CREATED)
async def create_seller_account(req: CreateSellerSchema, session: SessionDep):
    return await seller_service.register_seller(req_body=req, session=session)