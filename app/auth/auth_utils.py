import uuid
from datetime import timedelta, datetime

import jwt
from passlib.context import CryptContext
from app.config import security_settings


def generate_passwd_hash(password: str) -> str:
    pw_ctx = CryptContext(schemes=["bcrypt"])
    return pw_ctx.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    pw_ctx = CryptContext(schemes=["bcrypt"])
    return pw_ctx.verify(password, hashed_password)


def generate_token(user_data: dict, expiry: timedelta = None) -> str:
    access_token_expiry: int = 3600

    payload = {
        "user":user_data,
        "exp_time": (datetime.now() + (expiry if expiry is not None else timedelta(seconds=access_token_expiry))).isoformat(),
        "jti": str(uuid.uuid4())
    }

    token = jwt.encode(
        payload=payload,
        key=security_settings.JWT_SECRET,
        algorithm=security_settings.JWT_ALGORITHM
    )

    return token
