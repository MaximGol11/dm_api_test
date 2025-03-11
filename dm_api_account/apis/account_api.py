from restclient.client import RestClient


class AccountApi(RestClient):
    
    def post_v1_account(self, json_data):
        """Create a new account.
        Returns:
            response
        """
        
        response = self.post(
            path='/v1/account',
            headers=self.headers,
            json=json_data
            )
        return response
    
    
    def put_v1_account_token(self, token):
        """Activate account.
        Returns:
            response
        """
        
        response = self.put(
            path=f'/v1/account/{token}',
            headers=self.headers,
            )
        return response
    
    
    def put_v1_account_email(self, json_data):
        """Change email.
        Returns:
            response
        """
        
        response = self.put(
            path='/v1/account/email',
            headers=self.headers,
            json=json_data
            )
        return response