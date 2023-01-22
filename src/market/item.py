import logging

from .base import BaseMarketAPI

logger = logging.getLogger(__name__)


class MarketItem(BaseMarketAPI):
    def __init__(self, item_object: dict, token: str):
        """
        :param item_object: Item object from search response
        """
        self.item_object = item_object
        self.API_URL += f'{self.item_object["item_id"]}/'
        super().__init__(token=token)

    def fast_buy(self) -> dict:
        response = self.api_request(
            "fast-buy",
            data={"price": self.item_object["price"]},
            request_method="POST",
        )
        return response
