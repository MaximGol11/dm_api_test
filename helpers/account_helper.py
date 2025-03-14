import time
from json import loads
from services.serv_api_mailhog import MailHogApi
from services.serv_dm_api_account import DMApiAccount


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
            if user_login == login:
                """
                Пришлось добавить новый параметр в функцию, так как для сброса пароля приходит не 'ConfirmationLinkUrl', а 'ConfirmationLinkUri'
                """
                if password_token_flag:
                    return user_data['ConfirmationLinkUri'].split('/')[-1]
                return user_data['ConfirmationLinkUrl'].split('/')[-1]

        return f"Токен для пользователя {login}, не был получен по почте."


    def register_and_activate_user(
            self,
            login: str,
            password: str,
            email: str
    ):
        json_data = {
            "login": login,
            "password": password,
            "email": email
        }

        response = self.dm_account_api.account_api.post_v1_account(json_data=json_data)
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
        json_data = {
            "login": login,
            "password": password,
            "email": email
        }

        response = self.dm_account_api.account_api.post_v1_account(json_data=json_data)
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
        login_data = {
            "login": login,
            "password": password,
            "remember_me": remember_me
        }

        response = self.dm_account_api.login_api.post_v1_login(json_data=login_data)

        return response


    def auth_user(self, login, password):
        login_data = {
            "login": login,
            "password": password,
        }

        response = self.dm_account_api.login_api.post_v1_login(json_data=login_data)
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
        json_data = {
            "login": login,
            "password": password,
            "email": new_email
        }

        response = self.dm_account_api.account_api.put_v1_account_email(json_data=json_data)
        assert  response.status_code == 200

        return response


    def reset_user_password(
            self,
            login: str,
            email: str
    ):
        json_data = {
            "login": login,
            "email": email
        }

        response = self.dm_account_api.account_api.post_v1_account_password(json_data=json_data)
        assert response.status_code == 200

        return response


    def change_user_password(
            self,
            login: str,
            email: str,
            old_password: str,
            new_password: str
    ):
        json_data = {
            "login": login,
            "email": email
        }

        response = self.dm_account_api.account_api.post_v1_account_password(json_data=json_data)
        assert response.status_code == 200

        token = self.get_activation_token_by_login(login=login, password_token_flag=True)

        json_data = {
            "login": login,
            "token": token,
            "oldPassword": old_password,
            "newPassword": new_password
        }
        response = self.dm_account_api.account_api.put_v1_account_password(json_data=json_data)
        assert response.status_code == 200

        return response


    def get_user_account(self, **kwargs):
        response = self.dm_account_api.account_api.get_v1_account()

        return response
