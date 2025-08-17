# api/tests/test_booking.py
import allure
import pytest
from api.payloads import booking_payloads
from utils.allure_decorators import allure_annotations


# --- ТЕСТЫ ---

@allure_annotations(
    title="Успешное создание бронирования",
    story="Создание бронирования",
    description="Проверка создания бронирования с полным набором валидных данных.",
    severity=allure.severity_level.BLOCKER,
    tag="Positive"
)
def test_create_booking_positive(booking_endpoint) -> None:
    booking_endpoint.create_booking(booking_payloads.VALID_BOOKING)
    booking_endpoint.check_status_code_is_(200)
    booking_endpoint.check_firstname_is_(booking_payloads.VALID_BOOKING["firstname"])


@allure_annotations(
    title="Негативные тесты создания бронирования",
    story="Создание бронирования",
    description="Проверка, что система возвращает ошибку при отправке некорректных данных.",
    severity=allure.severity_level.CRITICAL,
    tag="Negative"
)
@pytest.mark.parametrize(
    "payload, expected_status_code, test_id",
    booking_payloads.invalid_booking_data(),
    ids=booking_payloads.invalid_booking_data_ids()
)
def test_create_booking_negative(booking_endpoint, payload, expected_status_code, test_id) -> None:
    booking_endpoint.create_booking(payload)
    booking_endpoint.check_status_code_is_(expected_status_code)


@allure_annotations(
    title="Успешное получение списка всех бронирований",
    story="Получение бронирования",
    description="Проверка эндпоинта получения списка всех бронирований.",
    severity=allure.severity_level.NORMAL,
    tag="Positive"
)
def test_get_all_bookings_positive(booking_endpoint, booking_id) -> None:
    booking_endpoint.get_all_bookings()
    booking_endpoint.check_status_code_is_(200)
    booking_endpoint.check_response_is_a_list_()


@allure_annotations(
    title="Негативный тест: Попытка обновить бронирование с невалидным токеном",
    story="Авторизация",
    description="Проверка, что система не позволяет изменять данные без авторизации.",
    severity=allure.severity_level.BLOCKER,
    tag="Negative"
)
def test_update_booking_with_invalid_token_negative(booking_endpoint, booking_id) -> None:
    booking_endpoint.update_booking(booking_id, booking_payloads.UPDATE_BOOKING, "invalid_token_12345")
    booking_endpoint.check_status_code_is_(403)


@allure_annotations(
    title="Негативный тест: Попытка обновить бронирование с невалидным токеном",
    story="Авторизация",
    description="Проверка, что система не позволяет изменять данные без авторизации.",
    severity=allure.severity_level.BLOCKER,
    tag="Negative"
)
@allure_annotations(
    title="Успешное частичное обновление бронирования",
    story="Обновление бронирования",
    description="Проверка частичного обновления данных ранее созданного бронирования.",
    severity=allure.severity_level.CRITICAL,
    tag="Positive"
)
def test_partial_update_booking_positive(booking_endpoint, booking_id, auth_token) -> None:
    # Действие 1: Частично обновляем бронирование
    booking_endpoint.partial_update_booking(booking_id, booking_payloads.PARTIAL_UPDATE_BOOKING, auth_token)
    booking_endpoint.check_status_code_is_(200)

    # Действие 2: Получаем обновленное бронирование, чтобы проверить все поля
    booking_endpoint.get_booking_by_id(booking_id)
    booking_endpoint.check_status_code_is_(200)

    # Проверка 1: Убеждаемся, что обновленные поля изменились
    booking_endpoint.check_firstname_is_(booking_payloads.PARTIAL_UPDATE_BOOKING["firstname"])

    # Проверка 2: Убеждаемся, что НЕобновленные поля остались прежними
    booking_endpoint.check_lastname_is_(booking_payloads.VALID_BOOKING["lastname"])


@allure_annotations(
    title="Негативный тест: Частичное обновление с невалидным токеном",
    story="Авторизация",
    description="Проверка, что система не позволяет частично изменять данные без авторизации.",
    severity=allure.severity_level.BLOCKER,
    tag="Negative"
)
def test_partial_update_booking_invalid_token_negative(booking_endpoint, booking_id) -> None:
    booking_endpoint.partial_update_booking(
        booking_id,
        booking_payloads.PARTIAL_UPDATE_BOOKING,
        "invalid_token_12345"
    )
    booking_endpoint.check_status_code_is_(403)


@allure_annotations(
    title="Негативный тест: Частичное обновление несуществующего бронирования",
    story="Обновление бронирования",
    description="Проверка ответа системы при попытке обновить несуществующий ресурс.",
    severity=allure.severity_level.NORMAL,
    tag="Negative"
)
def test_partial_update_non_existent_booking_negative(booking_endpoint, auth_token) -> None:
    booking_endpoint.partial_update_booking(
        99999999,
        booking_payloads.PARTIAL_UPDATE_BOOKING,
        auth_token
    )
    booking_endpoint.check_status_code_is_(405)  # API возвращает 405 Method Not Allowed, а не 404


@allure_annotations(
    title="Негативный тест: Частичное обновление с невалидными данными",
    story="Обновление бронирования",
    description="Проверка, что система возвращает ошибку при отправке некорректных данных.",
    severity=allure.severity_level.CRITICAL,
    tag="Negative"
)
@pytest.mark.parametrize(
    "payload, expected_status_code, test_id",
    booking_payloads.invalid_patch_data(),
    ids=booking_payloads.invalid_patch_data_ids()
)
def test_partial_update_with_bad_data_negative(booking_endpoint, booking_id, auth_token, payload, expected_status_code,
                                               test_id) -> None:
    booking_endpoint.partial_update_booking(booking_id, payload, auth_token)
    booking_endpoint.check_status_code_is_(expected_status_code)
