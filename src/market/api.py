from typing import Optional, Tuple
import re

from src.market.types import BearerToken, Headers
from .base import BaseMarketAPI, Response


class MarketAPI(BaseMarketAPI):
    def __init__(self, token: str):
        self._headers = Headers(authorization=BearerToken(token))

    @property
    def headers(self) -> dict:
        return self._headers

    def search(self, category: str, search_params: str) -> Response:
        response = self.api_request(f'{category}/{search_params}')
        return response

    @staticmethod
    def parse_search_data(search_url: str) -> Optional[Tuple[str, str]]:
        parse = re.search(r'https://lzt.market/([\w\-]+)/(.+)', search_url)
        if not parse:
            raise TypeError('Format search URL is invalid')
        category, search_params = parse.groups()
        return category, search_params
