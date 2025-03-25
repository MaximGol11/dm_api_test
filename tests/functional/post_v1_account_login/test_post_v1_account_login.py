import allure

from checkers.http_checkers import check_status_code_http


@allure.suite("Тесты проверки авторизации пользователя POST /v1/account/login")
class TestPostV1Account:

    @allure.title("Тест проверки авторизации пользователя")
    def test_post_v1_accounts_login(account_helper, prepare_user):
        login = prepare_user.login
        password = prepare_user.password
        email = prepare_user.email

        with check_status_code_http(400, "One or more validation errors occurred."):
            account_helper.user_login(login=login, password=password, validate_response=False)

        with check_status_code_http():
            account_helper.register_and_activate_user(login=login, password=password, email=email)
            account_helper.user_login(login=login, password=password)
