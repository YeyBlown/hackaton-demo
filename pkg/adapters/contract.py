# TODO: config logic here


import os


class PostgresEnv:
    username = os.getenv('POSTGRES_USERNAME')
    password = os.getenv('POSTGRES_PASSWORD')
    address = os.getenv('POSTGRES_ADDRESS')
    port = os.getenv('POSTGRES_PORT')
    database = os.getenv('POSTGRES_DATABASE_NAME')

    url_format = 'postgresql://{username}:{password}@{address}:{port}/{database}'
    url = url_format.format(username=username, password=password, address=address, port=port, database=database)

    @staticmethod
    def get_url():
        return PostgresEnv.url
