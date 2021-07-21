import re

from novelsave.exceptions import MissingSource
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

    raise MissingSource(url)


def parse_metasource(url):
    """
    create neta source object to which the :param url: belongs to

    :return: meta source object
    """
    for source in meta_sources:
        if source.of(url):
            return source()

    raise MissingSource(url, metadata=True)


def slugify(s, replace=''):
    return re.sub(r'[\\/:*"\'<>|.%$^&£?]', replace, s)
