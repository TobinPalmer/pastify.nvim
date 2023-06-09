from .type import Config


def validate_config(config: Config, logger, filetype: str) -> bool:
    c = config
    o = c['options']

    if filetype not in c["ft"]:
        logger(
            "Not in a filetype configured in config.options.ft",
            "WARN")
        return False

    if c is None:
        return False

    if o["apikey"] == "":
        logger(
            "You need to get a free API key for this plugin to work,\
                    get one at https://api.imgbb.com/", "WARN")
        return False

    if o["online"] is True and o["computer"] is True:
        logger(
            "Both online and computer cannot be true", "WARN")
        return False
    return True
