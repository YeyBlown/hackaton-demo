from passlib.context import CryptContext


class HashUtils:
    # TODO: ensure thread safe
    # TODO: move hard variables to contract, please :)
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @staticmethod
    def verify_password(plain_password, hashed_password):
        return HashUtils.pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password):
        return HashUtils.pwd_context.hash(password)
