

def test_put_v1_accounts_email(account_helper, prepare_user):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email
    new_email = f"new_{email}"

    account_helper.register_and_activate_user(login=login, password=password, email=email)
    account_helper.user_login(login=login, password=password)
    account_helper.change_user_email(login=login, password=password, new_email=new_email)

    response = account_helper.user_login(login=login, password=password)
    assert response.status_code == 403

    account_helper.activate_user(login=login)
    account_helper.user_login(login=login, password=password)