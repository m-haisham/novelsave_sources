class SourcesException(Exception):
    """Base exception of this package from which all other exceptions are derived from."""


class BadResponseException(SourcesException):
    """thrown when an unexpected response is received"""


class UnknownSourceException(SourcesException):
    """thrown when the url does not correspond to an existing source"""


class UnavailableException(SourcesException):
    """thrown when a function is unavailable"""


class ChapterException(SourcesException):
    """thrown when something unexpected happens during chapter update"""
