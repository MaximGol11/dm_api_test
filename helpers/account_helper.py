import time
from json import loads

import allure

from dm_api_account.models.login_credentials import LoginCredentials
from dm_api_account.models.registration import Registration
from services.serv_api_mailhog import MailHogApi
from services.serv_dm_api_account import DMApiAccount
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


class AccountHelper:

    def __init__(
            self,
            dm_account_api: DMApiAccount,
            mailhog_api: MailHogApi
    ):
        self.dm_account_api = dm_account_api
        self.mailhog_api = mailhog_api


    @retrier
    @allure.step("Получение активационного токена из письма")
    def get_activation_token_by_login(self, login, password_token_flag: bool = False):
        response = self.mailhog_api.mailhog_api.get_api_v2_messages()
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
    def register_and_activate_user(
            self,
            login: str,
            password: str,
            email: str
    ):
        registration = Registration(login=login, password=password, email=email)

        response = self.dm_account_api.account_api.post_v1_account(registration=registration)
        assert response.status_code == 201

        token = self.get_activation_token_by_login(login)

        response = self.dm_account_api.account_api.put_v1_account_token(token=token)

        return response


    @allure.step("Регистрация нового пользователя")
    def register_user_not_activate(
            self,
            login: str,
            password: str,
            email: str
    ):
        registration = Registration(login=login, password=password, email=email)

        response = self.dm_account_api.account_api.post_v1_account(registration=registration)
        assert response.status_code == 201

        return response


    @allure.step("Активация пользователя")
    def activate_user(self, login: str):
        token = self.get_activation_token_by_login(login=login)

        response = self.dm_account_api.account_api.put_v1_account_token(token=token)

        return response


    @allure.step("Авторизация пользователя")
    def user_login(
            self,
            login: str,
            password: str,
            remember_me: bool = True,
            validate_response: bool = True
    ):
        login_credentials = LoginCredentials(login=login, password=password, remember_me=remember_me)

        response = self.dm_account_api.login_api.post_v1_login(login_credentials=login_credentials, validate_response=validate_response)

        return response


    @allure.step("Авторизация пользователя с добавлением токена в хедеры")
    def auth_user(
            self,
            login,
            password,
            remember_me: bool = True
    ):
        login_credentials = LoginCredentials(login=login, password=password, remember_me=remember_me)

        response = self.dm_account_api.login_api.post_v1_login(login_credentials=login_credentials, validate_response=False)
        token = {
            "X-Dm-Auth-Token": response.headers["X-Dm-Auth-Token"]
        }
        self.dm_account_api.account_api.set_headers(token)
        self.dm_account_api.login_api.set_headers(token)


    @allure.step("Логаут пользователя из аккаунта пользователя и удаление токена из хедеров")
    def logout_user(self):
        response = self.dm_account_api.login_api.delete_v1_account_login()
        self.dm_account_api.account_api.del_token_in_headers()
        self.dm_account_api.login_api.del_token_in_headers()
        return response


    @allure.step("Логаут пользователя из аккаунта пользователя со всех устройств и удаление токена из хедеров")
    def logout_user_all(self):
        response = self.dm_account_api.login_api.delete_v1_account_login_all()
        self.dm_account_api.account_api.del_token_in_headers()
        self.dm_account_api.login_api.del_token_in_headers()
        return response


    @allure.step("Замена email пользователя на новый")
    def change_user_email(
            self,
            login: str,
            password: str,
            new_email: str
    ):
        сhange_email = ChangeEmail(login=login, password=password, email=new_email)

        response = self.dm_account_api.account_api.put_v1_account_email(сhange_email=сhange_email)

        return response


    @allure.step("Сброс пароля пользователя")
    def reset_user_password(
            self,
            login: str,
            email: str
    ):
        reset_password = ResetPassword(login=login, email=email)

        response = self.dm_account_api.account_api.post_v1_account_password(reset_password=reset_password)

        return response


    @allure.step("Замена пароля пользователя на новый")
    def change_user_password(
            self,
            login: str,
            email: str,
            old_password: str,
            new_password: str
    ):
        reset_password = ResetPassword(login=login, email=email)

        response = self.dm_account_api.account_api.post_v1_account_password(reset_password=reset_password)

        token = self.get_activation_token_by_login(login=login, password_token_flag=True)

        change_password = ChangePassword(
            login=login,
            token=token,
            old_password=old_password,
            new_password=new_password
            )
        
        response = self.dm_account_api.account_api.put_v1_account_password(change_password=change_password)

        return response


    @allure.step("Получение информации о пользователе")
    def get_user_account(self, validate_response: bool = True,  **kwargs):
        response = self.dm_account_api.account_api.get_v1_account(validate_response=validate_response, **kwargs)

        return response
