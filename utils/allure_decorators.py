import allure
import pytest

def allure_annotations(title: str, description: str, story: str, severity: allure.severity_level, tag: str):
    def decorator(func):
        func = allure.title(title)(func)
        func = allure.description(description)(func)
        func = allure.feature("API Тесты")(func)
        func = allure.story(story)(func)
        func = allure.severity(severity)(func)
        func = pytest.mark.api(func)
        func = pytest.mark.tag(tag.lower())(func)
        return func
    return decorator