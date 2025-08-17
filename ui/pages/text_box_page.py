# ui/pages/text_box_page.py
import allure
from playwright.sync_api import Page, expect
from ui.pages.base_page import BasePage


class TextBoxPage(BasePage):
    # Относительный URL для этой конкретной страницы
    relative_url = "/text-box"

    def __init__(self, page: Page):
        # Вызываем конструктор родительского класса BasePage
        super().__init__(page)
        # --- ЛОКАТОРЫ ЭЛЕМЕНТОВ ---
        # Мы определяем их здесь один раз
        self.full_name_input = page.locator("#userName")
        self.email_input = page.locator("#userEmail")
        self.current_address_textarea = page.locator("#currentAddress")
        self.permanent_address_textarea = page.locator("#permanentAddress")
        self.submit_button = page.locator("#submit")

        # --- ЛОКАТОРЫ РЕЗУЛЬТАТА ---
        self.output_name = page.locator("#output #name")
        self.output_email = page.locator("#output #email")

    # --- МЕТОДЫ-ДЕЙСТВИЯ (Actions) ---

    @allure.step("Заполнение поля 'Full Name' значением: {full_name}")
    def fill_full_name(self, full_name: str):
        self.full_name_input.fill(full_name)

    @allure.step("Заполнение поля 'Email' значением: {email}")
    def fill_email(self, email: str):
        self.email_input.fill(email)

    @allure.step("Нажатие на кнопку 'Submit'")
    def click_submit(self):
        self.submit_button.click()

    # --- КОМБИНИРОВАННЫЙ БИЗНЕС-МЕТОД ---

    @allure.step("Заполнение и отправка формы Text Box")
    def fill_and_submit_form(self, full_name: str, email: str):
        """Высокоуровневый метод, который инкапсулирует несколько действий."""
        self.fill_full_name(full_name)
        self.fill_email(email)
        self.click_submit()

    # --- МЕТОДЫ-ПРОВЕРКИ (Assertions) ---

    @allure.step("Проверка: В результате отображается имя '{expected_name}'")
    def check_output_name_is_(self, expected_name: str):
        # Playwright's expect инкапсулирует ожидания и проверки
        expect(self.output_name).to_have_text(f"Name:{expected_name}")

    @allure.step("Проверка: В результате отображается email '{expected_email}'")
    def check_output_email_is_(self, expected_email: str):
        expect(self.output_email).to_have_text(f"Email:{expected_email}")