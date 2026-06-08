from typing import Annotated

from fastapi import Depends, HTTPException, status

from app.auth.auth_utils import decode_token
from app.database.session import SessionDep
from app.model.seller_model import SellerModel
from app.security.security import oauth2_scheme


def get_access_token(token: Annotated[str, Depends(oauth2_scheme)]):
    data = decode_token(token)
    if data is None:
        raise HTTPException(
            detail="Invalid or expired access token",
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    return data


async def get_current_seller(token_data: Annotated[dict, Depends(get_access_token)], session: SessionDep):
    return await session.get(SellerModel, token_data["user"]["id"])


SellerDep = Annotated[SellerModel, Depends(get_current_seller)]