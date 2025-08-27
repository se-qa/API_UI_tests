import allure
from playwright.sync_api import Page, expect

from ui.pages.base_page import BasePage


class FormPage(BasePage):
    relative_url = "/automation-practice-form"

    def __init__(self, page: Page):
        super().__init__(page)

        self.input_first_name = page.get_by_role("textbox", name="First Name")
        self.input_last_name = page.get_by_role("textbox", name="Last Name")
        self.input_email = page.locator("#userEmail")
        self.input_number = page.locator("#userNumber")
        self.submit_button = page.get_by_role("button", name="Submit")

    def get_field_by_name(self, field_name: str):
        """Вспомогательный метод для получения локатора по строковому имени."""
        fields = {
            "first_name": self.input_first_name,
            "last_name": self.input_last_name,
            "email": self.input_email
        }
        if field_name not in fields:
            raise ValueError(f"Поле с именем '{field_name}' не найдено.")
        return fields[field_name]

    @allure.step("Заполнить поле First Name значением: {first_name}")
    def fill_first_name(self, first_name: str):
        self.input_first_name.fill(first_name)

    @allure.step("Заполнить поле Last Name значением: {last_name}")
    def fill_last_name(self, last_name: str):
        self.input_last_name.fill(last_name)

    @allure.step("Заполнить поле Email значением: {email}")
    def fill_email(self, email: str):
        self.input_email.fill(email)

    @allure.step("Заполнить поле Email значением: {mob_number}")
    def fill_mob_number(self, mob_number: str):
        self.input_number.fill(mob_number)

    @allure.step("Нажатие на кнопку 'Submit'")
    def click_submit(self):
        self.submit_button.click()

    @allure.step("Проверка валидации поля {field_name}")
    def check_field_is_valid_(self, field_name):
        expect(field_name).to_have_css("border-color", "rgb(40, 167, 69)")

    @allure.step("Проверка валидации поля '{field_name}' (ошибка)")
    def check_field_is_invalid_(self, field_name: str):
        field_locator = self.get_field_by_name(field_name)
        expect(field_locator).to_have_css("border-color", "rgb(220, 53, 69)")
