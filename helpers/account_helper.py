from http.client import responses
from json import loads

from services.serv_api_mailhog import MailHogApi
from services.serv_dm_api_account import DMApiAccount


class AccountHelper:

    def __init__(
            self,
            dm_account_api: DMApiAccount,
            mailhog_api: MailHogApi
    ):
        self.dm_account_api = dm_account_api
        self.mailhog_api = mailhog_api


    @staticmethod
    def get_activation_token_by_login(login, response):
        for item in response.json()['items']:
            user_data = loads(item['Content']['Body'])
            user_login = user_data['Login']
            if user_login == login:
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

        response = self.mailhog_api.mailhog_api.get_api_v2_messages()
        assert response.status_code == 200
        token = self.get_activation_token_by_login(login, response)

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
        response = self.mailhog_api.mailhog_api.get_api_v2_messages()
        assert response.status_code == 200
        token = self.get_activation_token_by_login(login=login, response=response)

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
        assert response.status_code == 200

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