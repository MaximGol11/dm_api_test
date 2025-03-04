from faker import Faker
from api_mailhog.apis.mailhog_api import MailhogApi
from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi



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
    
    


def get_activation_token_by_login(login, response):
    for item in response.json()['items']:
        if item['login'] == login:
            return item['token']
    return None