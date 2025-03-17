from dm_api_account.models.login_credentials import LoginCredentials
from restclient.client import RestClient


class LoginApi(RestClient):

    def post_v1_login(self, login_credentials: LoginCredentials):
        """Login in account.
        Returns:
            response
        """
        
        response = self.post(
            path='/v1/account/login',
            json=login_credentials.model_dump(exclude_none=True, by_alias=True)
        )
        return response


    def delete_v1_account_login(self, **kwargs):
        """Logout as current user.
        Returns:
            response
        """

        response = self.delete(
            path='/v1/account/login',
            **kwargs
        )
        return response


    def delete_v1_account_login_all(self, **kwargs):
        """Logout from every device.
        Returns:
            response
        """

        response = self.delete(
            path='/v1/account/login/all',
            **kwargs
        )
        return response