from faker import Faker
from api_mailhog.apis.mailhog_api import MailhogApi
from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi
from json import loads


def get_activation_token_by_login(login, response):
    for item in response.json()['items']:
        user_data = loads(item['Content']['Body'])
        user_login = user_data['Login']
        if user_login == login:
            return user_data['ConfirmationLinkUrl'].split('/')[-1]
        
    return f"Токен для пользователя {login}, не был получен по почте."


def test_post_v1_accounts():
    host = "http://5.63.153.31:5051"
    login = Faker().user_name()
    password = Faker().password()
    email = Faker().email()
    
    json_data = {
        "login": login,
        "password": password,
        "email": email
    }
    
    response = AccountApi(host).post_v1_account(json_data)
    assert response.status_code == 201
    
    response = MailhogApi("http://5.63.153.31:5025").get_api_v2_messages()
    assert response.status_code == 200
    
    token = get_activation_token_by_login(login, response)
    assert response.status_code == 200
    
    response = AccountApi(host).put_v1_account_token(token)
    
    response = LoginApi(host).post_v1_login({
        "login": login,
        "password": password
    })
    assert response.status_code == 200
    print(response.json())