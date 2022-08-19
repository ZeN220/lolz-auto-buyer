import json
import time
from abc import ABC, abstractmethod
from typing import Optional
from urllib import request, parse, error
from socket import error as SocketError

from src.base.errors import MarketBuyError, AuthorizationError
from src.base.types import Response


class BaseAPI(ABC):
    API_URL: str

    def api_request(self, method: str, data: Optional[dict] = None, request_method: Optional[str] = None) -> Response:
        if data is not None:
            data = parse.urlencode(data).encode()

        response = request.Request(
            url=f'{self.API_URL}/{method}',
            data=data, headers=self.headers, method=request_method
        )

        time.sleep(self.delay)
        try:
            with request.urlopen(response) as response:
                response = json.load(response)
                is_error = response.get('errors')
                if is_error:
                    raise MarketBuyError(is_error[0])
                return response

        except error.HTTPError as http_error:
            error_response = http_error.read().decode('utf-8')
            error_response = json.loads(error_response).get('errors')
            if error_response:
                raise MarketBuyError(error_response[0])
            raise AuthorizationError('Token is invalid')
        except (error.URLError, SocketError):
            # Server can be return a 104 socket error. This error will not affect the operation of the application
            return self.api_request(method, data, request_method)

    @property
    @abstractmethod
    def delay(self) -> int:
        ...

    @property
    @abstractmethod
    def headers(self) -> dict:
        ...
