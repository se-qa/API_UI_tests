import pytest
import allure
from playwright.sync_api import sync_playwright

from api.endpoints.auth_endpoint import AuthEndpoint
from api.endpoints.booking_endpoint import BookingEndpoint
from api.payloads import booking_payloads
from ui.pages.check_box_page import CheckBoxPage
from ui.pages.form_page import FormPage
from ui.pages.text_box_page import TextBoxPage
from utils.config import ADMIN_USERNAME, ADMIN_PASSWORD


# --- UI ФИКСТУРЫ ---

@pytest.fixture(scope="function")
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        new_page = browser.new_page()
        yield new_page
        browser.close()


def pytest_exception_interact(node, call, report):
    """
    Этот хук делает скриншот страницы в случае падения UI-теста и прикрепляет его к Allure-отчету.
    """
    # --- НОВАЯ, БОЛЕЕ НАДЕЖНАЯ ПРОВЕРКА ---
    # 1. Проверяем, есть ли у 'node' вообще атрибут 'funcargs' (т.е. является ли он функцией).
    # 2. И только потом проверяем, есть ли в этом словаре фикстура 'page'.
    if hasattr(node, "funcargs") and "page" in node.funcargs:
        page = node.funcargs["page"]
        # Делаем скриншот
        screenshot_bytes = page.screenshot()
        # Прикрепляем скриншот к отчету Allure
        allure.attach(
            screenshot_bytes,
            name=f"screenshot_on_failure_{node.name}",
            attachment_type=allure.attachment_type.PNG
        )


# --- API ФИКСТУРЫ ---

@pytest.fixture(scope="session")
def auth_endpoint() -> AuthEndpoint:
    return AuthEndpoint()


@pytest.fixture(scope="session")
def booking_endpoint() -> BookingEndpoint:
    return BookingEndpoint()


@pytest.fixture(scope="session")
def auth_token(auth_endpoint: AuthEndpoint) -> str:
    payload = {
        "username": ADMIN_USERNAME,
        "password": ADMIN_PASSWORD
    }
    token = auth_endpoint.get_token(payload)
    return token


@pytest.fixture(scope="function")
def booking_id(booking_endpoint: BookingEndpoint, auth_token: str) -> int:
    # --- SETUP ---
    payload = booking_payloads.VALID_BOOKING
    # Действие теперь возвращает ID напрямую
    created_booking_id = booking_endpoint.create_booking(payload)
    booking_endpoint.check_status_code_is_(200)
    # Убедимся, что ID действительно был получен
    assert created_booking_id is not None, "Не удалось создать бронирование в фикстуре"

    yield created_booking_id

    # --- TEARDOWN ---
    booking_endpoint.delete_booking(created_booking_id, auth_token)
    booking_endpoint.check_status_code_is_(201)


# --- ФИКСТУРЫ ДЛЯ PAGE OBJECTS ---
@pytest.fixture(scope="function")
def text_box_page(page) -> TextBoxPage:
    """Фикстура для создания экземпляра страницы Text Box."""
    return TextBoxPage(page)

@pytest.fixture(scope="function")
def check_box_page(page) -> CheckBoxPage:
    """Фикстура для создания экземпляра страницы Check Box."""
    return CheckBoxPage(page)

@pytest.fixture(scope="function")
def form_page(page) -> FormPage:
    """Фикстура для создания экземпляра страницы Form Page."""
    return FormPage(page)