from novelsave_sources.sources import sources, meta_sources
from novelsave_sources.exceptions import UnknownSourceException


def parse_source(url):
    """Locate and create a source parser for the url if schema exists

    :throws UnknownSourceException: if the url cannot be parsed by any existing source schema
    """
    for source in sources:
        if source.of(url):
            return source()

    raise UnknownSourceException(f'"{url}" does not correspond to any available source')


def parse_metasource(url: str):
    """Locate and create a source parser for the url if schema exists

    :throws UnknownSourceException: if the url cannot be parsed by any existing source schema
    """
    for source in meta_sources:
        if source.of(url):
            return source()

    raise UnknownSourceException(f'"{url}" does not correspond to any available metadata source')