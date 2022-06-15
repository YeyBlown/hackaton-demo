import string
import random


class UserSimulator:

    def __init__(self, min_posts, max_posts, min_likes, max_likes):
        self.number_of_posts = random.randint(min_posts, max_posts)
        self.number_of_likes = random.randint(min_likes, max_likes)
        self.username = self._get_random_string(12)
        self.password = self._get_random_string(12)

    def get_number_of_posts(self):
        return self.number_of_posts

    def get_number_of_likes(self):
        return self.number_of_likes

    def get_username(self):
        return self.username

    def get_password(self):
        return self.password

    def get_next_post_data(self):
        header, content = self._get_random_string(100), self._get_random_string(100)
        return header, content

    def _get_random_string(self, length: int):
        # choose from all lowercase letter
        result_str = ''.join(random.choice(string.ascii_lowercase) for _ in range(length))
        return result_str