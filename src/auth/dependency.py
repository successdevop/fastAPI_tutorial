from fastapi import Request, status
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from fastapi.exceptions import HTTPException
from src.utils.utils import UtilsService


class AccessTokenBearer(HTTPBearer):
    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)


    async def __call__(self, request: Request):
        creds = await super().__call__(request)
        token = creds.credentials

        token_data = UtilsService.decode_token(token)
        if not self._validate_token:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid or expired token"
            )

        if token_data["refresh"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide an access token"
            )

        return token_data

    def _validate_token(self, token: str) -> bool:
        token_data = UtilsService.decode_token(token)
        return True if token_data is not None else False