import pkg_resources

__version__ = pkg_resources.get_distribution('novelsave-sources').version

from .exceptions import (
    SourcesException, BadResponseException, UnknownSourceException,
    UnavailableException, ChapterException,
)

from .models import Novel, Volume, Chapter, Metadata

from .sources import (
    Source, MetaSource,
    sources, meta_sources
)

from .utils import (
    parse_source, parse_metasource,
    novel_source_types, metadata_source_types,
    locate_novel_source, locate_metadata_source,
)
