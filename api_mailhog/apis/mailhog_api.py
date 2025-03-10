from restclient.client import RestClient


class MailhogApi(RestClient):
        
    
    def get_api_v2_messages(self):
        """Get all emails from Mailhog.

        Returns:
            _type_: _description_
        """

        params = {
            "limit": 50
        }

        response = self.get(
            path='/api/v2/messages',
            headers=self.headers,
            params=params,
            verify=False
            )
        return response