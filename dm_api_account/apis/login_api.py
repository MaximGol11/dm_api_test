from restclient.client import RestClient


class LoginApi(RestClient):
        
    
    def post_v1_login(self, json_data):
        """Login in account.
        Returns:
            response
        """
        
        response = self.post(
            path='/v1/account/login',
            headers=self.headers,
            json=json_data
            )
        return response