# api/endpoints/base_api.py
import allure
from requests import Response
from pydantic import BaseModel, ValidationError
from typing import Any

class BaseApi:
    response: Response
    validated_response: Any

    @allure.step("Проверка: Статус-код ответа равен {expected_code}")
    def check_status_code_is_(self, expected_code: int) -> None:
        actual_code = self.response.status_code
        assert actual_code == expected_code, \
            f"Ожидался статус-код {expected_code}, но получен {actual_code}. Тело ответа: {self.response.text}"

    def validate_response_(self, schema: type[BaseModel]) -> None:
        """
        Валидирует ответ по Pydantic схеме.
        В случае ошибки, просто позволяет исключению ValidationError 'пролететь' дальше.
        """
        step_title = f"Проверка: Тело ответа валидируется по схеме {schema.__name__}"
        with allure.step(step_title):
            self.validated_response = schema(**self.response.json())