from abc import ABC


class BaseField(ABC):
    def __setattr__(self, key, value):
        if isinstance(value, str) and value.isdigit():
            value = int(value)
        super().__setattr__(key, value)
