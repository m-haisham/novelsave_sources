from ..exceptions import UnknownSourceException

from novelsave_sources.sources.metadata import meta_sources
from novelsave_sources.sources.novel import sources


def parse_source(url):
    """
    create source object to which the :param url: belongs to

    :return: source object
    """
    for source in sources:
        if source.of(url):
            return source()

    raise UnknownSourceException(f'"{url}" does not correspond to any available source')


def parse_metasource(url):
    """
    create neta source object to which the :param url: belongs to

    :return: meta source object
    """
    for source in meta_sources:
        if source.of(url):
            return source()

    raise UnknownSourceException(f'"{url}" does not correspond to any available metadata source')

