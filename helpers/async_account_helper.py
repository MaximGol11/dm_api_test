import asyncio
import functools
import time
from json import loads

import allure

from api_mailhog.async_apis.async_mailhog_api import AsyncMailhogApi
from dm_api_account.models.login_credentials import LoginCredentials
from dm_api_account.models.registration import Registration
from services.async_serv_api_mailhog import AsyncServMailHogApi
from services.async_serv_dm_api_account import AsyncServDMApiAccount
from dm_api_account.models.change_email import ChangeEmail
from dm_api_account.models.reset_password import ResetPassword
from dm_api_account.models.change_password import ChangePassword


def retrier(func):
    def wrapper(*args, **kwargs):
        token = None
        count = 0
        while token is None:
            print(f"Получаю токен пользователя из сервиса MailHog, попытка номер: {count}")
            token = func(*args, **kwargs)
            if token:
                return token
            if count == 5:
                raise AssertionError("Колличество попыток получения токена превышено")
            count += 1
            time.sleep(1)

    return wrapper


def async_retrier(max_attempts=5, delay=1.0):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            token = None
            for attempt in range(1, max_attempts + 1):
                print(f"Получаю токен, попытка {attempt}")
                token = await func(*args, **kwargs)
                if token:
                    return token
                await asyncio.sleep(delay)
            raise AssertionError("Количество попыток получения токена превышено")
        return wrapper
    return decorator


class AsyncAccountHelper:

    # def __init__(
    #         self,
    #         dm_account_api: AsyncServDMApiAccount,
    #         mailhog_api: AsyncServMailHogApi
    # ):
    #     self.dm_account_api = dm_account_api
    #     self.mailhog_api = mailhog_api


    def __init__(self, dm_account_api, mailhog_api):
        self.dm_account_api = dm_account_api
        self.mailhog_api = mailhog_api

    @async_retrier(max_attempts=5, delay=1)
    @allure.step("Получение активационного токена из письма")
    async def get_activation_token_by_login(self, login, password_token_flag: bool = False):
        response = await self.mailhog_api.get_api_v2_messages()
        assert response.status_code == 200

        token = None

        for item in response.json()['items']:
            user_data = loads(item['Content']['Body'])
            user_login = user_data.get('Login')
            if user_login == login:
                key = 'ConfirmationLinkUri' if password_token_flag else 'ConfirmationLinkUrl'
                token = user_data.get(key, "").split('/')[-1]
                if token:
                    return token


    @allure.step("Регистрация и активация нового пользователя")
    async def register_and_activate_user(
            self,
            login: str,
            password: str,
            email: str
    ):
        registration = Registration(login=login, password=password, email=email)

        response = await self.dm_account_api.post_v1_account(registration=registration)
        #assert response.status_code == 201

        token = await self.get_activation_token_by_login(login)

        response = await self.dm_account_api.put_v1_account_token(token=token)

        return response


    @allure.step("Регистрация нового пользователя")
    async def register_user_not_activate(
            self,
            login: str,
            password: str,
            email: str
    ):
        registration = Registration(login=login, password=password, email=email)

        response = await self.dm_account_api.post_v1_account(registration=registration)
        #assert response.status_code == 201

        return response


    @allure.step("Активация пользователя")
    async def activate_user(self, login: str):
        token = await self.get_activation_token_by_login(login=login)

        response = await self.dm_account_api.account_api.put_v1_account_token(token=token)

        return response


    @allure.step("Авторизация пользователя")
    async def user_login(
            self,
            login: str,
            password: str,
            remember_me: bool = True,
            validate_response: bool = True
    ):
        login_credentials = LoginCredentials(login=login, password=password, remember_me=remember_me)

        response = await self.dm_account_api.async_post_v1_login(
            login_credentials=login_credentials,
            validate_response=validate_response
        )
        return response


    @allure.step("Авторизация пользователя с добавлением токена в хедеры")
    async def auth_user(
            self,
            login,
            password,
            remember_me: bool = True
    ):
        login_credentials = LoginCredentials(login=login, password=password, remember_me=remember_me)

        response = await self.dm_account_api.login_api.post_v1_login(
            login_credentials=login_credentials,
            validate_response=False
        )
        token = {
            "X-Dm-Auth-Token": response.headers["X-Dm-Auth-Token"]
        }
        self.dm_account_api.account_api.set_headers(token)
        self.dm_account_api.account_api.set_headers(token)


    # @allure.step("Логаут пользователя из аккаунта пользователя и удаление токена из хедеров")
    # async def logout_user(self):
    #     response = await self.dm_account_api.login_api.delete_v1_account_login()
    #     self.dm_account_api.login_api.del_token_in_headers()
    #     self.dm_account_api.login_api.del_token_in_headers()
    #     return response
    #
    #
    # @allure.step("Логаут пользователя из аккаунта пользователя со всех устройств и удаление токена из хедеров")
    # async def logout_user_all(self):
    #     response = await self.dm_account_api.delete_v1_account_login_all()
    #     self.dm_account_api.del_token_in_headers()
    #     self.dm_account_api.del_token_in_headers()
    #     return response


    @allure.step("Замена email пользователя на новый")
    async def change_user_email(
            self,
            login: str,
            password: str,
            new_email: str
    ):
        change_email = ChangeEmail(login=login, password=password, email=new_email)

        response = await self.dm_account_api.account_api.put_v1_account_email(сhange_email=change_email)

        return response


    @allure.step("Сброс пароля пользователя")
    async def reset_user_password(
            self,
            login: str,
            email: str
    ):
        reset_password = ResetPassword(login=login, email=email)

        response = await self.dm_account_api.account_api.post_v1_account_password(reset_password=reset_password)

        return response

    @allure.step("Замена пароля пользователя на новый")
    async def change_user_password(
            self,
            login: str,
            email: str,
            old_password: str,
            new_password: str
    ):
        reset_password = ResetPassword(login=login, email=email)

        response = await self.dm_account_api.account_api.post_v1_account_password(reset_password=reset_password)

        token = await self.get_activation_token_by_login(login=login, password_token_flag=True)

        change_password = ChangePassword(
            login=login,
            token=token,
            old_password=old_password,
            new_password=new_password
        )

        response = await self.dm_account_api.account_api.put_v1_account_password(change_password=change_password)

        return response

    @allure.step("Получение информации о пользователе")
    async def get_user_account(self, validate_response: bool = True, **kwargs):
        response = await self.dm_account_api.account_api.get_v1_account(validate_response=validate_response, **kwargs)

        return response
