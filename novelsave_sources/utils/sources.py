import importlib
import inspect
from functools import lru_cache
from pathlib import Path
from typing import List, Type, TypeVar

from ..exceptions import UnknownSourceException
from ..sources import MetaSource, Source

_T = TypeVar("_T")


@lru_cache()
def _find_impl(r_location: str, interface: Type[_T]) -> List[Type[_T]]:
    """Finds the implementations of the interface in the provided package location"""
    impls = []
    package = r_location.replace("../", ".").replace("/", ".").rstrip(".")
    for path in (Path(__file__) / r_location).resolve().glob("*.py"):
        if not path.is_file():
            continue
        elif path.name.startswith("_"):  # private files
            continue

        module = importlib.import_module(
            f"{package}.{path.stem}", "novelsave_sources.utils"
        )
        for name, member in inspect.getmembers(module, inspect.isclass):
            # the member/class must be a subclass of interface and should be an implementation
            if (
                issubclass(member, interface)
                and member is not interface
                and not inspect.isabstract(member)
            ):
                impls.append(member)

    return impls


def novel_source_types() -> List[Type[Source]]:
    """Return all the available novel source types

    The first usage may be slow as it searches for all the
    source implementations and caches the results.

    :return: All the novel source scraper implementations
    :rtype: List[Type[Source]]
    """
    return _find_impl("../../sources/novel", Source)


def locate_novel_source(url: str) -> Type[Source]:
    """Locate and return the novel source parser for the url if it is supported

    :param url: Url pointing to the novel or the chapter needing to be
        scraped.
    :type url: str

    :return: Specific novel scraper that supports the url provided.
    :rtype: Type[Source]

    :raises UnknownSourceException: if the url cannot be parsed by any existing source schema
    """
    for source in novel_source_types():
        if source.of(url):
            return source

    raise UnknownSourceException(f'"{url}" does not correspond to any available source')


def metadata_source_types() -> List[Type[MetaSource]]:
    """Locate and return all the metadata source types

    The first usage may be slow as it searches for all the
    source implementations and caches the results.

    :return: All the metadata source scraper implementations
    :rtype: List[Type[MetaSource]]
    """
    return _find_impl("../../sources/metadata", MetaSource)


def locate_metadata_source(url: str) -> Type[MetaSource]:
    """Locate and return the metadata source parser for the url if it is supported

    :param url: Url pointing to the metadata profile.
    :type url: str

    :return: Specific metadata scraper that supports the url provided.
    :rtype: Type[MetaSource]

    :raises UnknownSourceException: if the url cannot be parsed by any existing source schema
    """
    for source in metadata_source_types():
        if source.of(url):
            return source

    raise UnknownSourceException(
        f'"{url}" does not correspond to any available metadata source'
    )
