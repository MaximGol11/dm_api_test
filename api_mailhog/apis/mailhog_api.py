import requests

class MailhogApi():
    
    def __init__(self, host, headers=None):
        self.host = host
        self.headers = headers
        
    
    def get_api_v2_messages(self):
        params = {
            "limit": 50
        }
        
        """Get all emails from Mailhog.

        Returns:
            _type_: _description_
        """
        
        response = requests.get(
            url=f'{self.host}/api/v2/messages',
            headers=self.headers,
            params=params,
            verify=False
            )
        return response