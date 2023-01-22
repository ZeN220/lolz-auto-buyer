import json
from typing import Optional
from urllib import parse, request


class TelegramAPI:
    API_URL: str = "https://api.telegram.org/bot"

    def __init__(self, bot_token: str):
        self.bot_token = bot_token
        self.API_URL += self.bot_token

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
            url=f"{self.API_URL}/{method}",
            data=request_data,
            method=request_method,
        )
        with request.urlopen(api_request) as response_object:
            response = json.load(response_object)
            return response

    def send_message(self, text: str, chat_id: int, **kwargs) -> dict:
        response = self.api_request(
            "sendMessage",
            {"text": text, "chat_id": chat_id, **kwargs},
        )
        return response
