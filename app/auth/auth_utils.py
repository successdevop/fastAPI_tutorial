from passlib.context import CryptContext

def generate_passwd_hash(password: str) -> str:
    pw_ctx = CryptContext(schemes=["bcrypt"])
    return pw_ctx.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    pw_ctx = CryptContext(schemes=["bcrypt"])
    return pw_ctx.verify(password, hashed_password)
