import allure
import json

def attach_response(response, name="Response"):
    try:
        body = json.dumps(response.json(), indent=4)
        allure.attach(body, name=name, attachment_type=allure.attachment_type.JSON)
    except json.JSONDecodeError:
        allure.attach(response.text, name=name, attachment_type=allure.attachment_type.TEXT)