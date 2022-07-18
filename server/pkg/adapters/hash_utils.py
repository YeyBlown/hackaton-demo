""" encryption utils module """
from passlib.context import CryptContext

from adapters.contract import EncryptionEnv


class HashUtils:
    """utils for hashing password and verifying password by hash"""

    pwd_context = CryptContext(
        schemes=[EncryptionEnv.get_hash_encryption_schema()], deprecated="auto"
    )

    @staticmethod
    def verify_password(plain_password, hashed_password):
        """verifies password by hash"""
        return HashUtils.pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password):
        """calculates password hash"""
        return HashUtils.pwd_context.hash(password)
