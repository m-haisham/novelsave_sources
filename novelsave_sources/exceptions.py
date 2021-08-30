class SourcesException(Exception):
    """base exception for this package"""


class BadResponseException(SourcesException):
    """thrown when an unexpected response is received"""


class UnknownSourceException(SourcesException):
    """thrown when the url does not correspond to an existing source"""


class UnavailableException(SourcesException):
    """thrown when a function is unavailable"""


class ChapterException(SourcesException):
    """thrown when something unexpected happens during chapter update"""
