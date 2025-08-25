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

        self.home_checkbox = page.locator("//span[text()='Home']")
        # Кнопки для раскрытия и сворачивания всего дерева
        self.expand_all_button = page.locator(".rct-option-expand-all")
        self.collapse_all_button = page.locator(".rct-option-collapse-all")

        # Чекбоксы по их названию (используем XPath для поиска по тексту)
        self.all_uncheck_checkboxes = page.locator(".rct-icon-uncheck")
        self.all_check_checkboxes = page.locator(".rct-icon-check")
        self.all_span_titles = page.locator(".rct-title")
        self.success_result_titles = page.locator(".text-success")

        # Область с результатами
        self.result_area = page.locator("//*[@id='result']")

    # --- МЕТОДЫ-ДЕЙСТВИЯ ---

    @allure.step("Выбор корневого чекбокса 'Home' (выбрать все)")
    def select_home_checkbox(self):
        self.home_checkbox.click()

    @allure.step("Раскрытие корневой директории 'Home'")
    def expand_home_directory(self):
        self.expand_toggle_button.click()

    @allure.step("Выбор чекбокса '{checkbox_name}'")
    def select_checkbox_by_name(self, checkbox_name: str):
        """
        Находит и кликает по чекбоксу, используя его видимое текстовое имя.
        :param checkbox_name: Текст чекбокса, например "Desktop" или "Downloads".
        """
        # Локатор создается динамически "на лету" на основе переданного имени
        checkbox_locator = self.page.locator(f"//span[text()='{checkbox_name}']")
        checkbox_locator.click()

    @allure.step("Раскрыть все дерево")
    def expand_all(self):
        self.expand_all_button.click()

    @allure.step("Скрыть все дерево")
    def collapse_all(self):
        self.collapse_all_button.click()

    # --- МЕТОДЫ-ПРОВЕРКИ ---

    @allure.step("Проверка: В результате отображается текст '{expected_text}'")
    def check_result_contains_text_(self, expected_text: str):
        """Проверяет, что в блоке с результатом есть нужный текст."""
        expect(self.result_area).to_contain_text(expected_text)

    @allure.step("Проверка: В результате НЕ отображается текст '{unexpected_text}'")
    def check_result_not_contains_text_(self, unexpected_text: str):
        """Проверяет, что в блоке с результатом нет ненужного текста."""
        expect(self.result_area).not_to_contain_text(unexpected_text)

    @allure.step("Проверка: Количество отмеченных и неотмеченных чекбоксов совпадает")
    def check_checked_and_unchecked_counts_are_equal(self):
        """
        Подсчитывает количество видимых иконок 'check' и 'uncheck' и сравнивает их.
        """
        # Playwright автоматически дождется появления элементов перед подсчетом
        unchecked_count = self.all_uncheck_checkboxes.count()
        self.home_checkbox.click()
        checked_count = self.all_check_checkboxes.count()
        result_box_titles = self.all_span_titles.count()

        # Добавляем в отчет Allure полезную информацию для отладки
        allure.attach(
            f"Количество отмеченных: {checked_count}\n"
            f"Количество неотмеченных: {unchecked_count}",
            name="Подсчет чекбоксов",
            attachment_type=allure.attachment_type.TEXT
        )

        # Выполняем саму проверку
        assert checked_count == unchecked_count and unchecked_count == checked_count, \
            f"Количество не совпадает! Отмечено: {checked_count}, Не отмечено: {unchecked_count}"

