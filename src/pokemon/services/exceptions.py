class InvalidStatus(Exception):
    pass


class NotFound(InvalidStatus):
    pass


class UnableToConnect(Exception):
    pass


class TooManyRequests(Exception):
    pass
