from novelsave_sources import (
    locate_metadata_source,
    locate_novel_source,
    metadata_source_types,
    novel_source_types,
)
from novelsave_sources.sources import MetaSource, Source
from novelsave_sources.sources.metadata.novelupdates import NovelUpdates
from novelsave_sources.sources.novel.webnovel import Webnovel


def test_novel_source_types():
    sources = novel_source_types()
    for source in sources:
        assert issubclass(source, Source)

    assert Webnovel in sources
    assert NovelUpdates not in sources


def test_locate_novel_source():
    source = locate_novel_source("https://www.webnovel.com/novel/")

    assert issubclass(source, Source)
    assert source == Webnovel


def test_metadata_source_types():
    sources = metadata_source_types()
    for source in sources:
        assert issubclass(source, MetaSource)

    assert Webnovel not in sources
    assert NovelUpdates in sources


def test_locate_metadata_source():
    source = locate_metadata_source("https://www.novelupdates.com/novel/")

    assert issubclass(source, MetaSource)
    assert source == NovelUpdates
