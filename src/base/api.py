import json
import time
from abc import ABC, abstractmethod
from typing import Optional
from urllib import request, parse, error

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
                return json.load(response)

        except error.HTTPError as http_error:
            error_response = http_error.read().decode('utf-8')
            return json.loads(error_response)
        except error.URLError:
            # Server can be return a 104 socket error. This error never see you at application work
            self.api_request(method, data, request_method)

    @property
    @abstractmethod
    def delay(self) -> int:
        ...

    @property
    @abstractmethod
    def headers(self) -> dict:
        ...
