import os

import dotenv

dotenv.load_dotenv('bot.env')


class UsersEnv:
    number_of_users = int(os.getenv('NUMBER_OF_USERS'))
    max_posts_per_user = int(os.getenv('MAX_POSTS_PER_USER'))
    max_likes_per_user = int(os.getenv('MAX_LIKES_PER_USER'))

    min_posts_per_user = int(os.getenv('MIN_POSTS_PER_USER', 1))
    min_likes_per_user = int(os.getenv('MIN_LIKES_PER_USER', 1))

    @staticmethod
    def get_number_of_users():
        return UsersEnv.number_of_users

    @staticmethod
    def get_max_posts_per_user():
        return UsersEnv.max_posts_per_user

    @staticmethod
    def get_max_likes_per_user():
        return UsersEnv.max_likes_per_user

    @staticmethod
    def get_min_posts_per_user():
        return UsersEnv.min_posts_per_user

    @staticmethod
    def get_min_likes_per_user():
        return UsersEnv.min_likes_per_user


class AppEnv:
    app_url = os.getenv('APP_URL')

    @staticmethod
    def get_app_url():
        return AppEnv.app_url