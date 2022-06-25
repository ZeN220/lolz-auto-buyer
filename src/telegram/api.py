from src.base import BaseAPI, Response


class TelegramAPI(BaseAPI):
    API_URL: str = 'https://api.telegram.org/bot'
    delay: int = 0

    def __init__(self, bot_token: str):
        self.bot_token = bot_token
        self.API_URL += self.bot_token

    @property
    def headers(self) -> dict:
        return {}

    def send_message(self, text: str, chat_id: int) -> Response:
        response = self.api_request('sendMessage', {'text': text, 'chat_id': chat_id})
        return response
