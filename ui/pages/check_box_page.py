# ui/pages/check_box_page.py
import allure
from playwright.sync_api import Page, expect
from ui.pages.base_page import BasePage


class CheckBoxPage(BasePage):
    relative_url = "/checkbox"

    def __init__(self, page: Page):
        super().__init__(page)
        # --- ЛОКАТОРЫ ЭЛЕМЕНТОВ ---
        # Кнопка для раскрытия/сворачивания дерева
        self.expand_toggle_button = page.locator("button[aria-label='Toggle']")

        # Чекбоксы по их названию (используем XPath для поиска по тексту)
        self.desktop_checkbox = page.locator("//span[text()='Desktop']")
        self.downloads_checkbox = page.locator("//span[text()='Downloads']")
        self.documents_checkbox = page.locator("//span[text()='Documents']")

        # Область с результатами
        self.result_area = page.locator("//*[@id='result']")

    # --- МЕТОДЫ-ДЕЙСТВИЯ ---

    @allure.step("Раскрытие корневой директории 'Home'")
    def expand_home_directory(self):
        self.expand_toggle_button.click()

    @allure.step("Выбор чекбокса 'Desktop'")
    def select_desktop_checkbox(self):
        self.desktop_checkbox.click()

    @allure.step("Выбор чекбокса 'Downloads'")
    def select_downloads_checkbox(self):
        self.downloads_checkbox.click()

    # --- МЕТОДЫ-ПРОВЕРКИ ---

    @allure.step("Проверка: В результате отображается текст '{expected_text}'")
    def check_result_contains_text_(self, expected_text: str):
        """Проверяет, что в блоке с результатом есть нужный текст."""
        expect(self.result_area).to_contain_text(expected_text)

    @allure.step("Проверка: В результате НЕ отображается текст '{unexpected_text}'")
    def check_result_not_contains_text_(self, unexpected_text: str):
        """Проверяет, что в блоке с результатом нет ненужного текста."""
        expect(self.result_area).not_to_contain_text(unexpected_text)