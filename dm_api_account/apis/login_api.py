import allure

from dm_api_account.models.login_credentials import LoginCredentials
from dm_api_account.models.user_envelope import UserEnvelope
from restclient.client import RestClient


class LoginApi(RestClient):

    @allure.step("Авторизация пользователя")
    def post_v1_login(self, login_credentials: LoginCredentials, validate_response: bool = True):
        """Login in account.
        Returns:
            response
        """
        
        response = self.post(
            path='/v1/account/login',
            json=login_credentials.model_dump(exclude_none=True, by_alias=True)
        )
        if validate_response:
            return UserEnvelope(**response.json())
        return response


    @allure.step("Логаут из аккаунта пользователя")
    def delete_v1_account_login(self, **kwargs):
        """Logout as current user.
        Returns:
            response
        """

        response = self.delete(
            path='/v1/account/login',
            **kwargs
        )
        return response


    @allure.step("Логаут из аккаунта пользователя, со всех устройств")
    def delete_v1_account_login_all(self, **kwargs):
        """Logout from every device.
        Returns:
            response
        """

        response = self.delete(
            path='/v1/account/login/all',
            **kwargs
        )
        return response