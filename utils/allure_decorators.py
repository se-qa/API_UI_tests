# utils/allure_decorators.py
import allure
import pytest
from typing import List

def allure_annotations(title: str, description: str, story: str, severity: allure.severity_level, tags: List[str]):
    """
    Универсальный декоратор для Allure и Pytest.
    Принимает список тегов. Первый тег используется для определения Feature (API/UI),
    а все теги из списка применяются как ПРЯМЫЕ маркеры pytest.

    :param tags: Список тегов, например ["UI", "Smoke", "Regression"]
    """
    if not tags:
        raise ValueError("Список тегов 'tags' не может быть пустым.")

    def decorator(func):
        # 1. Применяем стандартные аннотации Allure
        func = allure.title(title)(func)
        func = allure.description(description)(func)
        func = allure.story(story)(func)
        func = allure.severity(severity)(func)

        # 2. Определяем Feature по первому тегу в списке
        first_tag = tags[0].lower()
        if first_tag == "ui":
            func = allure.feature("UI Тесты")(func)
        elif first_tag == "api":
            func = allure.feature("API Тесты")(func)
        else:
            func = allure.feature(tags[0])

        # 3. Применяем ВСЕ теги из списка как прямые маркеры pytest
        for tag in tags:
            # Эта магия превращает строку 'smoke' в реальный объект маркера pytest.mark.smoke
            marker = getattr(pytest.mark, tag.lower())
            func = marker(func)

        return func
    return decorator