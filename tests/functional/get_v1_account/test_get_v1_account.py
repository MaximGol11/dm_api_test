
def test_get_v1_account_auth(auth_account_helper):
    response = auth_account_helper.get_user_account()
    assert response.status_code == 200