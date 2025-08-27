import allure
import requests
from utils.config import BASE_URL
from api.endpoints.base_api import BaseApi
from utils.api_helpers import attach_response


class AuthEndpoint(BaseApi):
    AUTH_URL = f"{BASE_URL}/auth"

    @allure.step("API: Получение токена авторизации")
    def get_token(self, payload: dict) -> str:
        self.response = requests.post(self.AUTH_URL, json=payload)
        attach_response(self.response, "Auth Response")
        token = self.response.json().get("token")
        assert token is not None, "Токен не был получен в ответе"
        return token
