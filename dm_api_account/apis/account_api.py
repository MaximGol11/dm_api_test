import requests

class AccountApi():
    
    def __init__(self, host, headers=None):
        self.host = host
        self.headers = headers
        
    
    def post_v1_account(self, json_data):
        """Create a new account.
        Returns:
            response
        """
        
        response = requests.post(
            url=f'{self.host}/v1/account',
            headers=self.headers,
            json=json_data
            )
        return response
    
    
    def put_v1_account_token(self, token):
        """Activate account.
        Returns:
            response
        """
        
        response = requests.put(
            url=f'{self.host}/v1/account/{token}',
            headers=self.headers
            )
        return response
    
    
    def put_v1_account_email(self, json_data):
        """Change email.
        Returns:
            response
        """
        
        response = requests.put(
            url=f'{self.host}/v1/account/email',
            headers=self.headers,
            json=json_data
            )
        return response