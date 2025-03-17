from restclient.client import RestClient


class AccountApi(RestClient):
    
    def post_v1_account(self, json_data):
        """Create a new account.
        Returns:
            response
        """
        
        response = self.post(
            path='/v1/account',
            json=json_data
            )
        return response

    def get_v1_account(self, **kwargs):
        """Get user account.
        Returns:
            response
        """

        response = self.get(
            path='/v1/account',
            **kwargs
        )
        return response
    
    
    def put_v1_account_token(self, token, **kwargs):
        """Activate account.
        Returns:
            response
        """
        
        response = self.put(
            path=f'/v1/account/{token}',
            **kwargs
            )
        return response
    
    
    def put_v1_account_email(self, json_data, **kwargs):
        """Change email.
        Returns:
            response
        """
        
        response = self.put(
            path='/v1/account/email',
            json=json_data,
            **kwargs
            )
        return response


    def post_v1_account_password(self, json_data, **kwargs):
        """Reset password.
         Returns:
             response
         """
        response = self.post(
            path='/v1/account/password',
            json=json_data,
            **kwargs
        )
        return response


    def put_v1_account_password(self, json_data, **kwargs):
        """Change password.
         Returns:
             response
         """

        response = self.put(
            path='/v1/account/password',
            json=json_data,
            **kwargs
        )
        return response