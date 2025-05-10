from dm_api_account.async_apis.async_account_api import AsyncAccountApi
from dm_api_account.async_apis.async_login_api import AsyncLoginApi
from restclient.configuration import Configuration

class AsyncServDMApiAccount:

    def __init__(
            self,
            configuration: Configuration
    ):
        self.configuration = configuration
        self.login_api = AsyncLoginApi(configuration=self.configuration)
        self.account_api = AsyncAccountApi(configuration=self.configuration)
# import allure
#
# from dm_api_account.models.change_email import ChangeEmail
# from dm_api_account.models.change_password import ChangePassword
# from dm_api_account.models.login_credentials import LoginCredentials
# from dm_api_account.models.registration import Registration
# from dm_api_account.models.reset_password import ResetPassword
# from dm_api_account.models.user_details_envelope import UserDetailsEnvelope
# from dm_api_account.models.user_envelope import UserEnvelope
# from restclient.async_client.async_client import AsyncRestClient
#
#
# class AsyncServDMApiAccount:
#     def __init__(self, client: AsyncRestClient):
#         self.client = client
#
#
#     def set_headers(self, headers):
#         self.client.headers.update(headers)
#
#     @allure.step("Регистрация нового пользователя")
#     async def post_v1_account(self, registration: Registration):
#         """Create a new account.
#         Returns:
#             response
#         """
#
#         response = await self.client.post(
#             path='/v1/account',
#             json=registration.model_dump(exclude_none=True, by_alias=True)
#         )
#         return response
#
#
#     @allure.step("Получение информации об авторизованном пользователе")
#     async def get_v1_account(self, validate_response: bool = True, **kwargs):
#         """Get user account.
#         Returns:
#             response
#         """
#
#         response = await self.client.get(
#             path='/v1/account',
#             **kwargs
#         )
#         if validate_response:
#             return UserDetailsEnvelope(**response.json())
#         return response
#
#
#     @allure.step("Активация аккаунт пользователя полученным токеном из письма")
#     async def put_v1_account_token(self, token, validate_response: bool = True, **kwargs):
#         """Activate account.
#         Returns:
#             response
#         """
#
#         response = await self.client.put(
#             path=f'/v1/account/{token}',
#             **kwargs
#         )
#         if validate_response:
#             return UserEnvelope(**response.json())
#         return response
#
#
#     @allure.step("Замена email пользователя на новый")
#     async def put_v1_account_email(self, change_email: ChangeEmail, validate_response: bool = True, **kwargs):
#         """Change email.
#         Returns:
#             response
#         """
#
#         response = await self.client.put(
#             path='/v1/account/email',
#             json=change_email.model_dump(exclude_none=True, by_alias=True),
#             **kwargs
#         )
#         if validate_response:
#             return UserEnvelope(**response.json())
#         return response
#
#
#     @allure.step("Сброс пароля пользователя")
#     async def post_v1_account_password(self, reset_password: ResetPassword, validate_response: bool = True, **kwargs):
#         """Reset password.
#          Returns:
#              response
#          """
#         response = await self.client.post(
#             path='/v1/account/password',
#             json=reset_password.model_dump(exclude_none=True, by_alias=True),
#             **kwargs
#         )
#         if validate_response:
#             return UserEnvelope(**response.json())
#         return response
#
#
#     @allure.step("Замена старого пароля пользователя на новый")
#     async def put_v1_account_password(self, change_password: ChangePassword, validate_response: bool = True, **kwargs):
#         """Change password.
#          Returns:
#              response
#          """
#
#         response = await self.client.put(
#             path='/v1/account/password',
#             json=change_password.model_dump(exclude_none=True, by_alias=True),
#             **kwargs
#         )
#         if validate_response:
#             return UserEnvelope(**response.json())
#         return response
#
#
#     @allure.step("Авторизация пользователя")
#     async def post_v1_login(self, login_credentials: LoginCredentials, validate_response: bool = True):
#         """Login in account.
#         Returns:
#             response
#         """
#
#         response = await self.client.post(
#             path='/v1/account/login',
#             json=login_credentials.model_dump(exclude_none=True, by_alias=True)
#         )
#         if validate_response:
#             return UserEnvelope(**response.json())
#         return response
#
#
#     @allure.step("Логаут из аккаунта пользователя")
#     async def delete_v1_account_login(self, **kwargs):
#         """Logout as current user.
#         Returns:
#             response
#         """
#
#         response = await self.client.delete(
#             path='/v1/account/login',
#             **kwargs
#         )
#         return response
#
#     @allure.step("Логаут из аккаунта пользователя, со всех устройств")
#     async def delete_v1_account_login_all(self, **kwargs):
#         """Logout from every device.
#         Returns:
#             response
#         """
#
#         response = await self.client.delete(
#             path='/v1/account/login/all',
#             **kwargs
#         )
#         return response