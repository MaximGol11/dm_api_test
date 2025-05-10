import allure
import pytest
from checkers.post_v1_account import PostV1Account


@allure.suite("Тесты на создание нового пользователя POST /v1/account")
class TestsPostV1Account:

    @allure.title("Проверка регистрации нового пользователя")
    @pytest.mark.asyncio
    async def test_async_post_v1_accounts(self, async_account_helper, user_parametrize_test_data):
        login = user_parametrize_test_data['login']
        password = user_parametrize_test_data['password']
        email = user_parametrize_test_data['email']
        expected_status_code = user_parametrize_test_data['expected_status']
        expected_message = "Validation failed"

        if expected_status_code == 200:
            await async_account_helper.register_and_activate_user(login=login, password=password, email=email)
            response = await async_account_helper.user_login(login=login, password=password)
            PostV1Account.check_response_values(login, response)
        else:
            response = await async_account_helper.register_user_not_activate(login=login, password=password, email=email)
            assert response.status_code == expected_status_code
            assert response.json()["title"] == expected_message
