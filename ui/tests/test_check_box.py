import allure
from utils.allure_decorators import allure_annotations


@allure_annotations(
    title="Успешный выбор чекбоксов в древовидной структуре",
    story="Форма Check Box",
    description="Этот тест раскрывает дерево, выбирает несколько чекбоксов и проверяет результат.",
    severity=allure.severity_level.CRITICAL,
    tag="UI"
)
# Запрашиваем нашу новую фикстуру check_box_page
def test_select_checkboxes_positive(check_box_page) -> None:
    # Действия
    check_box_page.open()
    check_box_page.expand_home_directory()
    check_box_page.select_desktop_checkbox()
    check_box_page.select_downloads_checkbox()

    # Проверки
    # Проверяем, что выбранные элементы появились в результате
    check_box_page.check_result_contains_text_("desktop")
    check_box_page.check_result_contains_text_("downloads")

    # Проверяем, что НЕвыбранные элементы НЕ появились в результате (очень важная проверка!)
    check_box_page.check_result_not_contains_text_("documents")