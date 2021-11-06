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


def test_novel_source_types():
    sources = novel_source_types()
    assert len(sources) != 0

    for source in sources:
        assert issubclass(source, Source)


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
    assert len(sources) != 0

    for source in sources:
        assert issubclass(source, MetaSource)


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
