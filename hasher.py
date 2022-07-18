from passlib.context import CryptContext


class Hasher():
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, plain_password: str, hashed_password: str):
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_hashed_password(self, plain_password):
        return self.pwd_context.hash(plain_password)
