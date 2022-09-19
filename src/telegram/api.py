import json
from typing import Optional

from urllib import request, parse


class TelegramAPI:
    API_URL: str = 'https://api.telegram.org/bot'

    def __init__(self, bot_token: str):
        self.bot_token = bot_token
        self.API_URL += self.bot_token

    def api_request(self, method: str, data: Optional[dict] = None, request_method: str = 'GET') -> dict:
        if data is not None:
            data = parse.urlencode(data).encode()
        response = request.Request(
            url=f'{self.API_URL}/{method}',
            data=data, method=request_method
        )
        with request.urlopen(response) as response:
            response = json.load(response)
            return response

    def send_message(self, text: str, chat_id: int) -> dict:
        response = self.api_request('sendMessage', {'text': text, 'chat_id': chat_id})
        return response
