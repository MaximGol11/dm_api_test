import allure

from restclient.async_client.async_client import AsyncRestClient


class AsyncMailhogApi:
    def __init__(self, client: AsyncRestClient):
        self.client = client

    @allure.step("Получаю список писем из почтового сервиса")
    async def get_api_v2_messages(self, limit=50, **kwargs):
        """Get all emails from Mailhog.

        Returns:
            _type_: _description_
        """

        params = {
            "limit": limit
        }

        response = await self.client.get(
            path='/api/v2/messages',
            params=params,
            #verify=False,
            **kwargs
            )
        return response