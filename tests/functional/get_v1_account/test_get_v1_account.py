import allure

from checkers.get_v1_account import GetV1Account
from checkers.http_checkers import check_status_code_http

@allure.suite("Тесты получения данных о пользователе GET /v1/account")
class TestGetV1Account:

    @allure.step("Тест проверки получения данных неавторизованного пользователя")
    def test_get_v1_account_non_auth(self, account_helper):
        with check_status_code_http(401, "User must be authenticated"):
            account_helper.get_user_account(validate_response=False)


    @allure.step("Тест проверки получения данных авторизованного пользователя")
    def test_get_v1_account_auth(self, auth_account_helper):
        with check_status_code_http():
            response = auth_account_helper.get_user_account()
        GetV1Account.check_response_values(response)


