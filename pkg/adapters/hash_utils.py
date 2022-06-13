from passlib.context import CryptContext

from adapters.contract import EncryptionEnv


class HashUtils:
    pwd_context = CryptContext(
        schemes=[EncryptionEnv.get_hash_encryption_schema()], deprecated="auto"
    )

    @staticmethod
    def verify_password(plain_password, hashed_password):
        return HashUtils.pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password):
        return HashUtils.pwd_context.hash(password)
