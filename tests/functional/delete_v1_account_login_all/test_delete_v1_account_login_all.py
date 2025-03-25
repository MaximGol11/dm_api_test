import allure

from checkers.http_checkers import check_status_code_http


@allure.suite("Тесты логаута пользователя со всех устройств DELETE /v1/account/login/all")
class TestDeleteV1AccountLoginAll:

    @allure.step("Тест логаута пользователя со всех устройств")
    def test_delete_v1_account_login_all(auth_account_helper):
        with check_status_code_http():
            auth_account_helper.logout_user_all()

        with check_status_code_http(401, "User must be authenticated"):
            auth_account_helper.get_user_account(validate_response=False)