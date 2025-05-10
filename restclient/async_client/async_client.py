import uuid
from json import JSONDecodeError

import curlify
import httpx
from restclient.configuration import Configuration
import structlog


class AsyncRestClient:
    def __init__(self, configuration: Configuration):
        self.host = configuration.host
        self.timeout = 10
        self.headers = configuration.headers or {}
        self.disable_log = configuration.disable_log
        self.client: httpx.AsyncClient | None = None
        self.log = structlog.getLogger(__name__).bind(service='api')


    async def open(self):
        """Создаёт httpx.AsyncClient"""
        self.client = httpx.AsyncClient(
            base_url=self.host,
            headers=self.headers,
            timeout=self.timeout
        )

    async def close(self):
        """Закрывает httpx.AsyncClient"""
        if self.client:
            await self.client.aclose()
            self.client = None

    def set_headers(self, headers):
        self.headers.update(headers)

    def add_token(self, token: str):
        """Добавляет токен в заголовки"""
        self.headers["Authorization"] = f"Bearer {token}"
        if self.client:
            self.client.headers["Authorization"] = f"Bearer {token}"

    async def request(self, method: str, path: str, validate_response: bool = True, **kwargs) -> httpx.Response:
        """Отправляет запрос к API"""
        log = self.log.bind(event_id=str(uuid.uuid4()))
        if not self.client:
            raise RuntimeError("Client not initialized. Call 'await open()' first.")

        if self.disable_log:
            rest_response = await self.client.request(method=method.upper(), url=path, **kwargs)
            rest_response.raise_for_status()
            return rest_response

        log.msg(
            event='Request',
            method=method,
            full_url=path,
            params=kwargs.get('params'),
            headers=kwargs.get('headers'),
            json=kwargs.get('json'),
            data=kwargs.get('data')
        )

        response = await self.client.request(method=method.upper(), url=path, **kwargs)
        # curl = curlify.to_curl(response.request)
        #
        # print(curl)

        log.msg(
            event="Response",
            status_code=response.status_code,
            headers=response.headers,
            json=self._get_json(response)
        )

        # if validate_response:
        #     response.raise_for_status()
        return response


    async def get(self, path, **kwargs):
        return await self.request("GET", path, **kwargs)

    async def post(self, path, **kwargs):
        return await self.request("POST", path, **kwargs)

    async def put(self, path, **kwargs):
        return await self.request("PUT", path, **kwargs)

    async def delete(self, path, **kwargs):
        return await self.request("DELETE", path, **kwargs)


    @staticmethod
    def _get_json(rest_response):
        try:
            return rest_response.json()
        except JSONDecodeError:
            return {}