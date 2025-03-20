

def test_post_v1_accounts_login(account_helper, prepare_user):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email

    response = account_helper.user_login(login=login, password=password, validate_response=False)
    assert response.status_code == 400

    account_helper.register_and_activate_user(login=login, password=password, email=email)
    account_helper.user_login(login=login, password=password)
