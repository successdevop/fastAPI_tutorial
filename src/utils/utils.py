from passlib.context import CryptContext


class UtilsService:
    def __init__(self):
        self._passwd_context = CryptContext(schemes=['bcrypt'])

    def hash_password_method(self, password: str) -> str:
        passwd_hash = self._passwd_context.hash(password)
        return passwd_hash

    def verify_password_method(self, password: str, hash_pw: str) -> bool:
        return self._passwd_context.verify(password, hash_pw)