import json
import time
from abc import ABC, abstractmethod
from socket import error as socket_error
from typing import Optional, Dict, Union, List
from urllib import request, parse, error

from .errors import MarketBuyError, AuthorizationError

Response = Dict[str, Union[str, int, List[dict]]]


class BaseMarketAPI(ABC):
    API_URL: str = 'https://api.lolz.guru/market'
    # Lolzteam API for market have a limit of 1 requests per 3 second
    delay: int = 3

    def api_request(
        self,
        method: str,
        data: Optional[dict] = None,
        request_method: str = 'GET'
    ) -> Response:
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
            # If error is empty, then the error is in the authorization
            raise AuthorizationError('Token is invalid')
        except (error.URLError, socket_error):
            """
            Server can be return a 104 socket error. 
            This error will not affect the operation of the application
            """
            return self.api_request(method, data, request_method)

    @property
    @abstractmethod
    def headers(self) -> dict:
        ...
