from typing import Any


class BaseSection:
    def __setattr__(self, key: str, value: Any) -> None:
        if isinstance(value, str) and value.isdigit():
            value = int(value)
        elif key.endswith("list"):
            values_list = value.split(",")
            value = list(map(str.strip, values_list))
        super().__setattr__(key, value)
