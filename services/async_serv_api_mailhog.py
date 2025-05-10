from api_mailhog.async_apis.async_mailhog_api import AsyncMailhogApi
from restclient.configuration import Configuration


class AsyncServMailHogApi:

    def __init__(
            self,
            configuration: Configuration
    ):
        self.configuration = configuration
        self.mailhog_api = AsyncMailhogApi(configuration=self.configuration)
