import logging

from src.base import BaseAPI, Response, MarketBuyError

logger = logging.getLogger(__name__)


class MarketItem(BaseAPI):
    API_URL: str = 'https://api.lolz.guru/market'
    delay: int = 3

    def __init__(self, item_object: dict, token: str):
        self.item_object = item_object
        self.token = token
        self._headers = {'Authorization': f'Bearer {self.token}'}
        self.API_URL += f'/{self.item_object["item_id"]}'

    @property
    def headers(self) -> dict:
        return self._headers

    @headers.setter
    def headers(self, value):
        raise ValueError('Headers cannot be set')

    def check(self) -> Response:
        response = self.api_request('check-account', request_method='POST')
        return response

    def reserve(self) -> Response:
        response = self.api_request('reserve', data={'price': self.item_object['price']}, request_method='POST')
        return response

    def cancel_reserve(self) -> Response:
        response = self.api_request('cancel-reserve', request_method='POST')
        return response

    def confirm_buy(self) -> Response:
        response = self.api_request('confirm-buy', request_method='POST')
        return response

    def buy(self) -> None:
        item_id = self.item_object['item_id']
        logger.info(f'Бронирую аккаунт {item_id}...')
        self.reserve()
        logger.info(f'Проверяю аккаунт {item_id}...')
        self.check()
        logger.info(f'Покупаю аккаунт {item_id}...')
        self.confirm_buy()
        logger.info(f'Аккаунт {item_id} успешно куплен!')
