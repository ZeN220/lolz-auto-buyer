import json
import logging
import time
from socket import error as socket_error
from typing import Optional
from urllib import error, parse, request

from .errors import MarketBuyError

logger = logging.getLogger(__name__)


class BaseMarketAPI:
    API_URL: str = "https://api.lzt.market/"
    # Lolzteam API for market have a limit of 1 requests per 3 second
    delay: int = 3

    def __init__(self, token: str, headers: Optional[dict] = None):
        self.token = token
        self.headers = headers or {}
        self.headers.setdefault("Authorization", f"Bearer {self.token}")

    def api_request(
        self,
        method: str,
        data: Optional[dict] = None,
        request_method: str = "GET",
    ) -> dict:
        if data is not None:
            request_data = parse.urlencode(data).encode()
        else:
            request_data = None
        api_request = request.Request(
            url=self.API_URL + method,
            data=request_data,
            headers=self.headers,
            method=request_method,
        )

        time.sleep(self.delay)
        try:
            with request.urlopen(api_request) as response_object:
                response = json.load(response_object)
                is_error = response.get("error")
                if is_error:
                    raise MarketBuyError(response["error_description"])
                return response

        except error.HTTPError as http_error:
            error_response = http_error.read().decode("utf-8")
            logger.warning("Получена ошибка: %s", error_response)
            try:
                error_response = json.loads(error_response).get("errors")
            except json.decoder.JSONDecodeError:
                """
                Some errors return body as HTML,
                so error is logged and called MarketBuyError
                to stop application
                """
                raise MarketBuyError("Получена неизвестная ошибка")
            raise MarketBuyError(error_response[0])
        except (error.URLError, socket_error):
            """
            Server can be return a 104 socket error.
            This error will not affect the operation of the application
            """
            return self.api_request(method, data, request_method)
