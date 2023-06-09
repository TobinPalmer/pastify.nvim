from typing import TypedDict, Literal


class Options(TypedDict):
    absolute_path: bool
    apikey: str
    local_path: str
    save: Literal["local", "online"]


class Config(TypedDict):
    opts: Options
    ft: dict[str, str]
