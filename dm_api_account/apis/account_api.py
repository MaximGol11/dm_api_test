import requests

class AccountApi():
    
    def __init__(self, host, headers=None):
        self.host = host
        self.headers = headers
        
    
    def post_v1_account(self, json_data):
        response = requests.post(url=f'{self.host}/v1/account', headers=self.headers, json=json_data)
        return response
    
    
    def put_v1_account_token(self, token):
        response = requests.put(url=f'{self.host}/v1/account/{token}', headers=self.headers)
        return response
    
    