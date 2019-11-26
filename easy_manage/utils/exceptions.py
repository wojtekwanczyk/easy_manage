# pylint: disable=missing-docstring


class BadHttpResponse(Exception):
    def __init__(self, status):
        super().__init__()
        self.status = status


class InvalidCredentials(Exception):
    pass


class NotInitializedError(Exception):
    pass
