import json

import requests

from services import AppEnv


class RequestService:

    def __init__(self):
        self.app_url = AppEnv.get_app_url()
        self.register_url = self.app_url + '/user/create'
        self.token_url = self.app_url + '/auth/token'
        self.create_post_url = self.app_url + '/post/create'
        self.create_like_url = self.app_url + '/post/like'

    def register_user(self, user):
        response = requests.post(self.register_url, json=user.get_create_request())
        return response

    def get_token(self, user):
        response = requests.post(self.token_url, data=user.get_login_request())
        token = json.loads(response.content)["access_token"]
        return token

    def create_post(self, user, token):
        header, content = user.get_next_post_data()
        response = requests.post(self.create_post_url, json={"header": header, "content": content}, headers={"Authorization": f"Bearer {token}"})
        return response

    def put_like(self, user, token, liked_code):
        url = self.create_like_url + f"?post_id={liked_code}"
        response = requests.post(url, headers={"Authorization": f"Bearer {token}"})
        return response
