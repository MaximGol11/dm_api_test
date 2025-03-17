from dm_api_account.models.registration import Registration
from restclient.client import RestClient
from dm_api_account.models.change_email import ChangeEmail
from dm_api_account.models.reset_password import ResetPassword
from dm_api_account.models.change_password import ChangePassword

class AccountApi(RestClient):
    
    def post_v1_account(self, registration: Registration):
        """Create a new account.
        Returns:
            response
        """
        
        response = self.post(
            path='/v1/account',
            json=registration.model_dump(exclude_none=True, by_alias=True)
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
    
    
    def put_v1_account_email(self, сhange_email: ChangeEmail, **kwargs):
        """Change email.
        Returns:
            response
        """
        
        response = self.put(
            path='/v1/account/email',
            json=сhange_email.model_dump(exclude_none=True, by_alias=True),
            **kwargs
            )
        return response


    def post_v1_account_password(self, reset_password: ResetPassword, **kwargs):
        """Reset password.
         Returns:
             response
         """
        response = self.post(
            path='/v1/account/password',
            json=reset_password.model_dump(exclude_none=True, by_alias=True),
            **kwargs
        )
        return response


    def put_v1_account_password(self, change_password: ChangePassword, **kwargs):
        """Change password.
         Returns:
             response
         """

        response = self.put(
            path='/v1/account/password',
            json=change_password.model_dump(exclude_none=True, by_alias=True),
            **kwargs
        )
        return response