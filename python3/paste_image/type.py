from typing import TypedDict


class Options(TypedDict):
    computer: bool
    default_name: bool
    local_path: str
    online: bool
    apikey: str


class Config(TypedDict):
    options: Options
    ft: dict[str, str]
