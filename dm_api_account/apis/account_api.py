from dm_api_account.models.registration import Registration
from dm_api_account.models.user_details_envelope import UserDetailsEnvelope
from dm_api_account.models.user_envelope import UserEnvelope
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

    def get_v1_account(self, validate_response: bool = True, **kwargs):
        """Get user account.
        Returns:
            response
        """

        response = self.get(
            path='/v1/account',
            **kwargs
        )
        if validate_response:
            return UserDetailsEnvelope(**response.json())
        return response
    
    
    def put_v1_account_token(self, token, validate_response: bool = True, **kwargs):
        """Activate account.
        Returns:
            response
        """
        
        response = self.put(
            path=f'/v1/account/{token}',
            **kwargs
            )
        if validate_response:
            return UserEnvelope(**response.json())
        return response
    
    
    def put_v1_account_email(self, сhange_email: ChangeEmail, validate_response: bool = True, **kwargs):
        """Change email.
        Returns:
            response
        """
        
        response = self.put(
            path='/v1/account/email',
            json=сhange_email.model_dump(exclude_none=True, by_alias=True),
            **kwargs
            )
        if validate_response:
            return UserEnvelope(**response.json())
        return response


    def post_v1_account_password(self, reset_password: ResetPassword, validate_response: bool = True, **kwargs):
        """Reset password.
         Returns:
             response
         """
        response = self.post(
            path='/v1/account/password',
            json=reset_password.model_dump(exclude_none=True, by_alias=True),
            **kwargs
        )
        if validate_response:
            return UserEnvelope(**response.json())
        return response


    def put_v1_account_password(self, change_password: ChangePassword, validate_response: bool = True, **kwargs):
        """Change password.
         Returns:
             response
         """

        response = self.put(
            path='/v1/account/password',
            json=change_password.model_dump(exclude_none=True, by_alias=True),
            **kwargs
        )
        if validate_response:
            return UserEnvelope(**response.json())
        return response