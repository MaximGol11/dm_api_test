import allure

from checkers.http_checkers import check_status_code_http


@allure.suite("Тесты смены пароля PUT /v1/account/password")
class TestPutV1AccountPassword:

    @allure.title("Тест смены пароля пользователя")
    def test_put_v1_account_password(self, account_helper, prepare_user_faker):
        login = prepare_user_faker.login
        password = prepare_user_faker.password
        email = prepare_user_faker.email
        new_password = f'{password}_new'

        with check_status_code_http():
            account_helper.register_and_activate_user(login=login, password=password, email=email)
            account_helper.auth_user(login=login, password=password)
            account_helper.change_user_password(login=login, email=email, old_password=password, new_password=new_password)

        with check_status_code_http(400, "One or more validation errors occurred."):
            account_helper.user_login(login=login, password=password, validate_response=False)


        with check_status_code_http():
            account_helper.auth_user(login=login, password=new_password)
            account_helper.get_user_account()

