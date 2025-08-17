import allure
from playwright.sync_api import Page, expect

class BasePage:
    BASE_URL = "https://demoqa.com"

    def __init__(self, page: Page):
        self.page = page
        # self.url - будет определяться в дочерних классах
        self.url = f"{self.BASE_URL}{getattr(self, 'relative_url', '')}"

    @allure.step("Открытие страницы по URL: {url}")
    def open(self, url: str = None):
        """Открывает URL страницы. Если URL не передан, используется URL из класса."""
        target_url = url or self.url
        self.page.goto(target_url)

    @allure.step("Проверка, что заголовок страницы содержит текст '{text}'")
    def check_title_contains(self, text: str):
        """Проверяет, что заголовок страницы (title) содержит определенный текст."""
        expect(self.page).to_have_title(text)