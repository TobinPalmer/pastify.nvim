from typing import TypedDict, Literal


class Options(TypedDict):
    absolute_path: bool
    apikey: str
    local_path: str
    save: Literal["local", "online", "local_file"]
    filename: str
    default_ft: str


class Config(TypedDict):
    opts: Options
    ft: dict[str, str]
