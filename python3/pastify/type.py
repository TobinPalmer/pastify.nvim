from typing import TypedDict, Literal


class Options(TypedDict):
    local_path: str
    save: Literal["local", "online"]
    apikey: str


class Config(TypedDict):
    opts: Options
    ft: dict[str, str]
