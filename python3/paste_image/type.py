from typing import TypedDict


class Options(TypedDict):
    computer: bool
    default_name: bool
    local_path: str
    markdown_image: bool
    markdown_standard: bool
    online: bool
    apikey: str


class Config(TypedDict):
    options: Options
