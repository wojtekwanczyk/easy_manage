# pylint: disable=missing-docstring


class BadHttpResponse(Exception):
    pass


class InvalidCredentials(Exception):
    pass


class NotInitializedError(Exception):
    pass


class ProtocolNotHandled(Exception):
    pass
