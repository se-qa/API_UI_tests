import allure
import requests
from typing import Optional

from pydantic import ValidationError

from utils.config import BASE_URL
from api.endpoints.base_api import BaseApi
from api.models.booking_model import Booking, BookingResponse
from utils.api_helpers import attach_response


class BookingEndpoint(BaseApi):
    BOOKING_URL = f"{BASE_URL}/booking"

    @allure.step("API-действие: Создание нового бронирования")
    def create_booking(self, payload: dict) -> Optional[int]:
        allure.attach(str(payload), name="Request Payload", attachment_type=allure.attachment_type.JSON)
        self.response = requests.post(self.BOOKING_URL, json=payload)
        attach_response(self.response)

        if self.response.status_code == 200:
            try:
                self.validate_response_(BookingResponse)
                return self.validated_response.bookingid
            except ValidationError:
                return None
        return None

    @allure.step("API-действие: Удаление бронирования по ID '{booking_id}'")
    def delete_booking(self, booking_id: int, token: str) -> None:
        headers = {"Cookie": f"token={token}"}
        self.response = requests.delete(f"{self.BOOKING_URL}/{booking_id}", headers=headers)
        attach_response(self.response)

    @allure.step("API-действие: Получение бронирования по ID '{booking_id}'")
    def get_booking_by_id(self, booking_id: int) -> None:
        self.response = requests.get(f"{self.BOOKING_URL}/{booking_id}")
        attach_response(self.response)
        if self.response.status_code == 200:
            self.validate_response_(Booking)

    @allure.step("API-действие: Получение списка всех бронирований")
    def get_all_bookings(self) -> None:
        self.response = requests.get(self.BOOKING_URL)
        attach_response(self.response)

    @allure.step("API-действие: Обновление бронирования по ID '{booking_id}'")
    def update_booking(self, booking_id: int, payload: dict, token: str) -> None:
        allure.attach(str(payload), name="Request Payload", attachment_type=allure.attachment_type.JSON)
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Cookie": f"token={token}"
        }
        self.response = requests.put(f"{self.BOOKING_URL}/{booking_id}", json=payload, headers=headers)
        attach_response(self.response)
        if self.response.status_code == 200:
            self.validate_response_(Booking)

    @allure.step("API-действие: Частичное обновление бронирования по ID '{booking_id}'")
    def partial_update_booking(self, booking_id: int, payload: dict, token: str) -> None:
        allure.attach(str(payload), name="Request Payload", attachment_type=allure.attachment_type.JSON)
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Cookie": f"token={token}"
        }
        self.response = requests.patch(f"{self.BOOKING_URL}/{booking_id}", json=payload, headers=headers)
        attach_response(self.response)
        if self.response.status_code == 200:
            self.validate_response_(Booking)

    @allure.step("Проверка: Имя в ответе соответствует '{expected_name}'")
    def check_firstname_is_(self, expected_name: str) -> None:
        validated_data = self.validated_response.booking if isinstance(self.validated_response,
                                                                       BookingResponse) else self.validated_response
        actual_name = validated_data.firstname
        assert actual_name == expected_name, f"Ожидалось имя '{expected_name}', получено '{actual_name}'"

    @allure.step("Проверка: Ответ является непустым списком")
    def check_response_is_a_list_(self) -> None:
        response_json = self.response.json()
        assert isinstance(response_json, list), "Ответ не является списком"
        assert len(response_json) > 0, "Список бронирований в ответе пуст"

    @allure.step("Проверка: Фамилия в ответе соответствует '{expected_lastname}'")
    def check_lastname_is_(self, expected_lastname: str) -> None:
        validated_data = self.validated_response.booking if isinstance(self.validated_response,
                                                                       BookingResponse) else self.validated_response
        actual_lastname = validated_data.lastname
        assert actual_lastname == expected_lastname, (f"Ожидалась фамилия '{expected_lastname}', "
                                                      f"получено '{actual_lastname}'")
