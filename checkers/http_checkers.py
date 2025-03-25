import allure
import requests
from contextlib import contextmanager
from requests.exceptions import HTTPError


@contextmanager
@allure.step("Проверка статус кода ответа")
def check_status_code_http(expected_status_code: requests.codes = requests.codes.OK, expected_message: str = ""):
    try:
        yield
        if expected_status_code != requests.codes.OK:
            raise AssertionError(f"Ожидаемый статус код должен быть равен: {expected_status_code}")
        if expected_message:
            raise AssertionError(f"Ожидаемое сообщение должно быть равно: '{expected_message}'")
    except HTTPError as e:
        assert e.response.status_code == expected_status_code
        assert e.response.json()["title"] == expected_message