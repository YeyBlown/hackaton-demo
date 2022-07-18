import string
import random


class UserSimulator:

    def __init__(self, min_posts, max_posts, min_likes, max_likes):
        self.number_of_posts = random.randint(min_posts, max_posts)
        self.number_of_likes = random.randint(min_likes, max_likes)
        self.username = self._get_random_string(12)
        self.password = self._get_random_string(12)
        self.name = self._get_random_string(10)
        self.surname = self._get_random_string(10)
        self.description = self._get_random_string(10) if random.random() > 0.2 else None
        self.age = random.randint(1, 101)

    def get_number_of_posts(self):
        return self.number_of_posts

    def get_number_of_likes(self):
        return self.number_of_likes

    def get_username(self):
        return self.username

    def get_password(self):
        return self.password

    def get_name(self):
        return self.name

    def get_surname(self):
        return self.surname

    def get_age(self):
        return self.age

    def get_description(self):
        return self.description

    def get_next_post_data(self):
        header, content = self._get_random_string(100), self._get_random_string(100)
        return header, content

    def get_create_request(self):
        request = {
            "username": self.get_username(),
            "hashed_password": self.get_password(),
            "name": self.get_name(),
            "surname": self.get_surname(),
            "age": self.get_age()
        }
        if self.get_description():
            request["description"] = self.get_description()
        return request

    def get_login_request(self):
        return {
            "client_secret": "lol",
            "username": self.get_username(),
            "password": self.get_password(),
        }

    def _get_random_string(self, length: int):
        # choose from all lowercase letter
        result_str = ''.join(random.choice(string.ascii_lowercase) for _ in range(length))
        return result_str