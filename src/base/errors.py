class MarketBuyError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class AuthorizationError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)
