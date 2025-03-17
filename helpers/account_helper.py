import time
from json import loads

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
    def get_activation_token_by_login(self, login, password_token_flag: bool = False):
        response = self.mailhog_api.mailhog_api.get_api_v2_messages()
        assert response.status_code == 200

        for item in response.json()['items']:
            user_data = loads(item['Content']['Body'])
            user_login = user_data['Login']
            if user_login == login and password_token_flag == True:
                return user_data['ConfirmationLinkUri'].split('/')[-1]
            elif user_login == login:
                return user_data['ConfirmationLinkUrl'].split('/')[-1]
                """
                Пришлось добавить новый параметр в функцию, так как для сброса пароля приходит не 'ConfirmationLinkUrl', а 'ConfirmationLinkUri'
                """




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
        assert response.status_code == 200

        return response


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


    def activate_user(self, login: str):
        token = self.get_activation_token_by_login(login=login)

        response = self.dm_account_api.account_api.put_v1_account_token(token=token)

        return response


    def user_login(
            self,
            login: str,
            password: str,
            remember_me: bool = True
    ):
        login_credentials = LoginCredentials(login=login, password=password, remember_me=remember_me)

        response = self.dm_account_api.login_api.post_v1_login(login_credentials=login_credentials)

        return response


    def auth_user(
            self,
            login,
            password,
            remember_me: bool = True
    ):
        login_credentials = LoginCredentials(login=login, password=password, remember_me=remember_me)

        response = self.dm_account_api.login_api.post_v1_login(login_credentials=login_credentials)
        token = {
            "X-Dm-Auth-Token": response.headers["X-Dm-Auth-Token"]
        }
        self.dm_account_api.account_api.set_headers(token)
        self.dm_account_api.login_api.set_headers(token)


    def logout_user(self):
        response = self.dm_account_api.login_api.delete_v1_account_login()
        self.dm_account_api.account_api.del_token_in_headers()
        self.dm_account_api.login_api.del_token_in_headers()
        return response


    def logout_user_all(self):
        response = self.dm_account_api.login_api.delete_v1_account_login_all()
        self.dm_account_api.account_api.del_token_in_headers()
        self.dm_account_api.login_api.del_token_in_headers()
        return response


    def change_user_email(
            self,
            login: str,
            password: str,
            new_email: str
    ):
        сhange_email = ChangeEmail(login=login, password=password, email=new_email)

        response = self.dm_account_api.account_api.put_v1_account_email(сhange_email=сhange_email)
        assert  response.status_code == 200

        return response


    def reset_user_password(
            self,
            login: str,
            email: str
    ):
        reset_password = ResetPassword(login=login, email=email)

        response = self.dm_account_api.account_api.post_v1_account_password(reset_password=reset_password)
        assert response.status_code == 200

        return response


    def change_user_password(
            self,
            login: str,
            email: str,
            old_password: str,
            new_password: str
    ):
        reset_password = ResetPassword(login=login, email=email)

        response = self.dm_account_api.account_api.post_v1_account_password(reset_password=reset_password)
        assert response.status_code == 200

        token = self.get_activation_token_by_login(login=login, password_token_flag=True)

        change_password = ChangePassword(
            login=login,
            token=token,
            old_password=old_password,
            new_password=new_password
            )
        
        response = self.dm_account_api.account_api.put_v1_account_password(change_password=change_password)
        assert response.status_code == 200

        return response


    def get_user_account(self, **kwargs):
        response = self.dm_account_api.account_api.get_v1_account(**kwargs)

        return response
