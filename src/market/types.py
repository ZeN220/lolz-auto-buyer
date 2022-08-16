from dataclasses import dataclass


class BearerToken(str):
    """
    Данный класс нужен для валидации токена от Lolzteam.
    """

    def __new__(cls, token: str):
        if not token.startswith('Bearer '):
            token = f'Bearer {token}'
        obj = super().__new__(cls, token)
        return obj


@dataclass
class Headers(dict):
    Authorization: BearerToken

    def __post_init__(self):
        super().__init__(**self.__dict__)
