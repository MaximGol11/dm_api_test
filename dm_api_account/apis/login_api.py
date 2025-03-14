from restclient.client import RestClient


class LoginApi(RestClient):

    def post_v1_login(self, json_data):
        """Login in account.
        Returns:
            response
        """
        
        response = self.post(
            path='/v1/account/login',
            json=json_data
        )
        return response


    def delete_v1_account_login(self, **kwargs):
        """Logout as current user.
        Returns:
            response
        """

        response = self.delete(
            path='/v1/account/login'
        )
        return response


    def delete_v1_account_login_all(self, **kwargs):
        """Logout from every device.
        Returns:
            response
        """

        response = self.delete(
            path='/v1/account/login/all'
        )
        return response