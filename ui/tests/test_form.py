import allure
import pytest

from ui.data import form_data
from utils.allure_decorators import allure_annotations


@allure_annotations(
    title="Успешная валидация поля",
    story="Форма Form",
    description="Этот тест жмет кнопку Submit и проверяет валидацию поля Email",
    severity=allure.severity_level.NORMAL,
    tags=['UI', 'Regression']
)
def test_validation_email_positive(form_page) -> None:
    form_page.open()
    form_page.fill_email("shitov@gmail.com")
    form_page.fill_first_name("Evgen")
    form_page.fill_last_name("Shit")
    form_page.click_submit()
    form_page.check_field_is_valid_(form_page.input_email)
    form_page.check_field_is_valid_(form_page.input_first_name)
    form_page.check_field_is_valid_(form_page.input_last_name)


@allure_annotations(
    title="Негативные тесты валидации полей формы",
    story="Форма Form",
    description="Этот тест проверяет, что обязательные и некорректно заполненные поля подсвечиваются красным.",
    severity=allure.severity_level.CRITICAL,
    tags=['UI', 'Regression']
)
@pytest.mark.parametrize(
    "first_name, last_name, email, field_to_check, test_id",
    form_data.invalid_form_data(),
    ids=form_data.get_invalid_data_ids()
)
def test_form_fields_validation_negative(form_page, first_name, last_name, email, field_to_check, test_id):
    form_page.open()

    form_page.fill_first_name(first_name)
    form_page.fill_last_name(last_name)
    form_page.fill_email(email)

    form_page.click_submit()

    form_page.check_field_is_invalid_(field_to_check)
