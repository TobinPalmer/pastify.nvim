from .type import Config


def validate_config(config: Config, logger, filetype: str) -> bool:
    c = config
    opts = c['opts']

    if filetype not in c["ft"]:
        logger(
            "Not in a filetype configured in config.ft",
            "WARN")
        return False

    if c is None:
        return False

    if opts["apikey"] == "" and opts['save'] == 'online':
        logger(
            "You need to get a free API key for online saving, get one at https://api.imgbb.com/", "WARN")
        return False

    if opts["save"] != "local" and opts["save"] != 'online':
        logger(
            str(opts['save']), "WARN")
        return False
    return True
