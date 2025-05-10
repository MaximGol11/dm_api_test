import allure
import pytest


@allure.suite("Тесты проверки авторизации пользователя POST /v1/account/login")
class TestAsyncPostV1Account:

    @pytest.mark.asyncio
    @allure.title("Тест проверки авторизации пользователя")
    async def test_async_post_v1_accounts_login(self, async_account_helper, prepare_user):
        login = prepare_user.login
        password = prepare_user.password
        email = prepare_user.email

        response = await async_account_helper.user_login(login=login, password=password, validate_response=False)

        assert response.status_code == 400
        assert response.json()["title"] == "One or more validation errors occurred."

        await async_account_helper.register_and_activate_user(login=login, password=password, email=email)
        await async_account_helper.user_login(login=login, password=password)