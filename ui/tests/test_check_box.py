import allure
from utils.allure_decorators import allure_annotations


@allure_annotations(
    title="Успешный выбор чекбоксов в древовидной структуре",
    story="Форма Check Box",
    description="Этот тест раскрывает дерево, выбирает несколько чекбоксов и проверяет результат.",
    severity=allure.severity_level.CRITICAL,
    tags=['UI', 'Regression']
)
def test_select_checkboxes_positive(check_box_page) -> None:
    # Действия
    check_box_page.open()
    check_box_page.expand_home_directory()
    # Используем наш новый, универсальный метод
    check_box_page.select_checkbox_by_name("Desktop")
    check_box_page.select_checkbox_by_name("Downloads")

    # Проверки (остаются без изменений)
    check_box_page.check_result_contains_text_("desktop")
    check_box_page.check_result_contains_text_("downloads")
    check_box_page.check_result_not_contains_text_("documents")

@allure_annotations(
    title="Успешный выбор всех чекбоксов в древовидной структуре",
    story="Форма Check Box",
    description="Этот тест раскрывает дерево, выбирает несколько чекбоксов и проверяет результат.",
    severity=allure.severity_level.CRITICAL,
    tags=['UI']
)
def test_select_all_checkboxes_positive(check_box_page) -> None:
    # Действия
    check_box_page.open()
    check_box_page.expand_all()
    # Используем наш новый, универсальный метод
    check_box_page.check_checked_and_unchecked_counts_are_equal()