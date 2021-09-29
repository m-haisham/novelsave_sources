from novelsave_sources import novel_source_types, metadata_source_types, locate_novel_source, locate_metadata_source
from novelsave_sources.sources import Source, MetaSource
from novelsave_sources.sources.metadata import NovelUpdates
from novelsave_sources.sources.novel import Webnovel


def test_novel_source_types():
    sources = novel_source_types()
    for source in sources:
        assert issubclass(source, Source)

    assert Webnovel in sources
    assert NovelUpdates not in sources


def test_locate_novel_source():
    source = locate_novel_source('https://www.webnovel.com/novel/')

    assert issubclass(source, Source)
    assert source == Webnovel


def test_metadata_source_types():
    sources = metadata_source_types()
    for source in sources:
        assert issubclass(source, MetaSource)

    assert Webnovel not in sources
    assert NovelUpdates in sources


def test_locate_metadata_source():
    source = locate_metadata_source('https://www.novelupdates.com/novel/')

    assert issubclass(source, MetaSource)
    assert source == NovelUpdates
