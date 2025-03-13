

def test_put_v1_accounts_token(account_helper, prepare_user):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email

    account_helper.register_user_not_activate(login=login, password=password, email=email)

    response = account_helper.user_login(login=login, password=password)
    assert response.status_code == 403

    account_helper.activate_user(login=login)
    account_helper.user_login(login=login, password=password)