import logging
import uuid
from typing import Optional

import jwt
from datetime import timedelta, datetime
from passlib.context import CryptContext
from src.config import Config


class UtilsService:
    ACCESS_TOKEN_EXPIRY = 3600

    def __init__(self):
        self._passwd_context = CryptContext(schemes=['bcrypt'])

    def hash_password_method(self, password: str) -> str:
        passwd_hash = self._passwd_context.hash(password)
        return passwd_hash

    def verify_password_method(self, password: str, hash_pw: str) -> bool:
        return self._passwd_context.verify(password, hash_pw)

    @staticmethod
    def generate_access_token(user_data: dict, expiry: timedelta = None, refresh: bool = False) -> str:
        payload = {
            "user": user_data,
            "expiry_time": (datetime.now() + (
                expiry if expiry is not None else timedelta(seconds=UtilsService.ACCESS_TOKEN_EXPIRY))).isoformat(),
            "jti": str(uuid.uuid4()),
            "refresh_token": refresh
        }

        token = jwt.encode(
            payload=payload,
            key=Config.JWT_SECRET_KEY,
            algorithm=Config.JWT_ALGORITHM
        )

        return token

    @staticmethod
    def decode_token(token: str) -> Optional[dict]:
        try:
            token_data = jwt.decode(
                jwt=token,
                key=Config.JWT_SECRET_KEY,
                algorithms=[Config.JWT_ALGORITHM]
            )
            return token_data
        except jwt.PyJWTError as e:
            logging.exception(e)
            return None