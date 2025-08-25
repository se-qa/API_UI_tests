import allure
from utils.allure_decorators import allure_annotations

@allure_annotations(
    title="Успешное заполнение и проверка формы Text Box",
    story="Форма Text Box",
    description="Этот тест заполняет все поля формы Text Box и проверяет корректность отображения данных.",
    severity=allure.severity_level.BLOCKER,
    tags=['UI', 'Smoke', 'Regression']
)
# Теперь мы запрашиваем фикстуру text_box_page напрямую
def test_fill_text_box_form_positive(text_box_page) -> None:
    # Подготовка данных (остается в тесте, так как это данные, а не логика)
    full_name = "John Doe"
    email = "test@example.com"

    # Действия
    text_box_page.open()
    text_box_page.fill_and_submit_form(full_name, email)

    # Проверки
    text_box_page.check_output_name_is_(full_name)
    text_box_page.check_output_email_is_(email)