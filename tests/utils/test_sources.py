from unittest.mock import Mock

import pytest

from novelsave_sources import (
    locate_metadata_source,
    locate_novel_source,
    metadata_source_types,
    novel_source_types,
    UnknownSourceException,
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


def test_locate_novel_source(mocker):
    mock_source = Mock()
    mocker.patch(
        "novelsave_sources.utils.sources.novel_source_types", return_value=[mock_source]
    )

    mock_source.of.return_value = True
    source = locate_novel_source("/test/novel/url")
    assert source == mock_source

    mock_source.of.return_value = False
    with pytest.raises(UnknownSourceException):
        locate_novel_source("/test/novel/url")


def test_metadata_source_types():
    sources = metadata_source_types()
    for source in sources:
        assert issubclass(source, MetaSource)

    assert Webnovel not in sources
    assert NovelUpdates in sources


def test_locate_metadata_source(mocker):
    mock_source = Mock()
    mocker.patch(
        "novelsave_sources.utils.sources.metadata_source_types",
        return_value=[mock_source],
    )

    mock_source.of.return_value = True
    source = locate_metadata_source("/test/metadata/url")
    assert source == mock_source

    mock_source.of.return_value = False
    with pytest.raises(UnknownSourceException):
        locate_metadata_source("/test/metadata/url")
