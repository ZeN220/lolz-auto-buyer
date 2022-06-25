from typing import Optional, Tuple
import re

from src.base import BaseAPI, Response


class MarketAPI(BaseAPI):
    API_URL: str = 'https://api.lolz.guru/market'
    delay: int = 3

    def __init__(self, token: str):
        self.token = token
        self._headers = {'Authorization': f'Bearer {self.token}'}

    @property
    def headers(self) -> dict:
        return self._headers

    @headers.setter
    def headers(self, value):
        raise ValueError('Headers cannot be set')

    def search(self, category: str, search_params: str) -> Response:
        response = self.api_request(f'{category}/?{search_params}')
        return response

    @staticmethod
    def parse_search_data(search_url: str) -> Optional[Tuple[str, str]]:
        parse = re.findall(r'https://lolz.guru/market/(\w+)/\?(.+)', search_url)
        if not parse:
            raise TypeError('Format search URL is invalid')
        return parse[0]
