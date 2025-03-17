from restclient.client import RestClient


class MailhogApi(RestClient):

    def get_api_v2_messages(self, limit=50, **kwargs):
        """Get all emails from Mailhog.

        Returns:
            _type_: _description_
        """

        params = {
            "limit": limit
        }

        response = self.get(
            path='/api/v2/messages',
            params=params,
            verify=False,
            **kwargs
            )
        return response