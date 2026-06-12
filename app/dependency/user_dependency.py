from typing import Annotated

from fastapi import Depends, HTTPException, status

from app.auth.auth_utils import decode_token
from app.database.session import SessionDep
from app.model.delivery_model import DeliveryPartner
from app.model.seller_model import Seller
from app.security.security import oauth2_scheme, delivery_oauth2_scheme
from app.database.redis_conn import is_jti_blacklisted


async def _get_access_token(token: str):
    data = decode_token(token)
    if data is None or await is_jti_blacklisted(jti=data["jti"]):
        raise HTTPException(
            detail="Invalid or expired access token",
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    return data


async def get_seller_access_token(token: Annotated[str, Depends(oauth2_scheme)]):
    return await _get_access_token(token=token)


async def get_d_partner_access_token(token: Annotated[str, Depends(delivery_oauth2_scheme)]):
    return await _get_access_token(token=token)


async def get_current_seller(token_data: Annotated[dict, Depends(get_seller_access_token)], session: SessionDep):
    seller = await session.get(Seller, token_data["user"]["id"])
    if seller is None:
        raise HTTPException(detail="Not authorised", status_code=status.HTTP_401_UNAUTHORIZED)
    return seller

async def get_current_d_partner(token_data: Annotated[dict, Depends(get_d_partner_access_token)], session: SessionDep):
    partner = await session.get(DeliveryPartner, token_data["user"]["id"])
    if partner is None:
        raise HTTPException(detail="Not authorised", status_code=status.HTTP_401_UNAUTHORIZED)
    return partner


SellerDep = Annotated[Seller, Depends(get_current_seller)]
DeliveryPartnerDep = Annotated[DeliveryPartner, Depends(get_current_d_partner)]