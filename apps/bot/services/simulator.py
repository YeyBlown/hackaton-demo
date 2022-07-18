import random

from services import UsersEnv
from services import RequestService
from services import UserSimulator


class Simulator:

    def __init__(self):
        self.request_service = RequestService()

    def simulate(self):
        users = [UserSimulator(UsersEnv.get_min_posts_per_user(), UsersEnv.get_max_posts_per_user(), UsersEnv.get_min_likes_per_user(), UsersEnv.get_max_likes_per_user()) for _ in range(UsersEnv.get_number_of_users())]
        list(map(self.request_service.register_user, users))
        tokens = list(map(self.request_service.get_token, users))
        for user, token in zip(users, tokens):
            for _ in range(user.get_number_of_posts()):
                self.request_service.create_post(user, token)

        number_of_posts = sum([user.get_number_of_posts() for user in users])
        post_numbers = range(1, number_of_posts+1)
        for user, token in zip(users, tokens):
            user_likes = random.sample(post_numbers, min(user.get_number_of_likes(), number_of_posts))
            for liked_post in user_likes:
                self.request_service.put_like(user, token, liked_post)
