from importlib.metadata import version

__version__ = version('novelsave-sources')

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
    parse_source, parse_metasource, novel_source_types, locate_novel_source,
    metadata_source_types, locate_metadata_source
)