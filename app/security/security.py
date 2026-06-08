from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer, HTTPBearer

from app.auth.auth_utils import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/sellers/login")

# class AccessTokenBearer(HTTPBearer):
#     async def __call__(self, request):
#         auth_credentials = await super().__call__(request)
#         token = auth_credentials.credentials
#
#         token_data = decode_token(token=token)
#         if token_data is None:
#             raise HTTPException(
#                 detail="Invalid or expired access token",
#                 status_code=401
#             )
#
#         return token_data
#
#
# access_token_bearer = AccessTokenBearer()


