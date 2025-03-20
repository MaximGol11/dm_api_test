

def test_delete_v1_account_login_all(auth_account_helper):
    response = auth_account_helper.logout_user_all()
    assert response.status_code == 204
    response = auth_account_helper.get_user_account(validate_response=False)
    assert response.status_code == 401