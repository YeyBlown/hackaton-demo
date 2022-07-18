"""config logic here"""
# pylint: disable=missing-function-docstring,missing-class-docstring
import os
from dotenv import load_dotenv


load_dotenv("local.env")


class PostgresEnv:
    username = os.getenv("POSTGRES_USERNAME")
    password = os.getenv("POSTGRES_PASSWORD")
    address = os.getenv("POSTGRES_ADDRESS")
    port = os.getenv("POSTGRES_PORT")
    database = os.getenv("POSTGRES_DATABASE_NAME")

    url_format = "postgresql://{username}:{password}@{address}:{port}/{database}"
    url = url_format.format(
        username=username,
        password=password,
        address=address,
        port=port,
        database=database,
    )

    @staticmethod
    def get_url():
        return PostgresEnv.url

    @staticmethod
    def get_database():
        return PostgresEnv.database


class EncryptionEnv:
    hash_encryption_schema = os.getenv("HASH_ENCRYPTION_SCHEMA")
    token_url = os.getenv("TOKEN_URL")
    token_secret_key = os.getenv("TOKEN_SECRET_KEY")
    token_algorithm = os.getenv("TOKEN_ALGORITHM")
    access_token_expire_minutes = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

    @staticmethod
    def get_hash_encryption_schema():
        return EncryptionEnv.hash_encryption_schema

    @staticmethod
    def get_token_url():
        return EncryptionEnv.token_url

    @staticmethod
    def get_token_secret_key():
        return EncryptionEnv.token_secret_key

    @staticmethod
    def get_token_algorithm():
        return EncryptionEnv.token_algorithm

    @staticmethod
    def get_access_token_expire_minutes():
        return EncryptionEnv.access_token_expire_minutes


class DateTimeEnv:
    date_format = os.getenv("DATE_FORMAT")

    @staticmethod
    def get_date_format():
        return DateTimeEnv.date_format


class AppEnv:
    app_host = os.getenv("APP_HOST")
    app_port = int(os.getenv("APP_PORT"))

    @staticmethod
    def get_app_host():
        return AppEnv.app_host

    @staticmethod
    def get_app_port():
        return AppEnv.app_port
