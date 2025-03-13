

def test_post_v1_accounts(account_helper, prepare_user_faker):
    login = prepare_user_faker.login
    password = prepare_user_faker.password
    email = prepare_user_faker.email

    account_helper.register_and_activate_user(login=login, password=password, email=email)
    account_helper.user_login(login=login, password=password)