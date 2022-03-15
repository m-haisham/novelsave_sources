import argparse
from collections import namedtuple
import hashlib
from datetime import datetime, timedelta
import pickle
from typing import Optional
from requests import Response
from pathlib import Path
from novelsave_sources import locate_novel_source, locate_metadata_source
from novelsave_sources.exceptions import UnknownSourceException
from novelsave_sources.sources.metadata.metasource import MetaSource
from novelsave_sources.sources.novel.source import Source
from novelsave_sources.utils.gateways import BaseHttpGateway, DefaultHttpGateway
from pprint import pprint


# Cache

DIRECTORY = Path(__file__).parent.parent / ".cache/response"
DURATION = timedelta(days=1)


def make_key(
    method: str,
    url: str,
    headers: dict = None,
    params: dict = None,
    data: dict = None,
    json: dict = None,
):
    keys = [method, url]
    for map in [headers, params, data, json]:
        if map is None:
            continue

        for key, value in map.items():
            keys.append(f"{key}:{value}")

    return hashlib.sha1(";".join(keys).encode("utf-8")).hexdigest()


def get_file(key: str) -> Path:
    return DIRECTORY / f"{key}.crp"


def set_cache(key: str, response: Response):
    DIRECTORY.mkdir(parents=True, exist_ok=True)

    data = {
        "datetime": datetime.now(),
        "response": response,
    }

    with get_file(key).open("wb") as f:
        pickle.dump(data, f)


def get_cache(key: str) -> Optional[Response]:
    file = get_file(key)
    if not file.exists() or not file.is_file():
        return None

    with file.open("rb") as f:
        data = pickle.load(f)

    diff = datetime.now() - data["datetime"]
    if diff > DURATION:
        file.unlink()
        return None

    return data["response"]


class DebugGateway(DefaultHttpGateway):
    def __init__(self, cache: bool = True):
        super().__init__()
        self.cache = cache

    def request(
        self,
        method: str,
        url: str,
        headers: dict = None,
        params: dict = None,
        data: dict = None,
        json: dict = None,
    ) -> Response:
        flags = [
            ("H" if headers is not None else ""),
            ("P" if params is not None else ""),
            ("D" if data is not None else ""),
            ("J" if json is not None else ""),
        ]
        flags = " ".join([f for f in flags if f])
        if self.cache:
            key = make_key(method, url, headers, params, data, json)
        print(f"{method.upper()} {url} {flags}... ", end="")

        if self.cache:
            if response := get_cache(key):
                print("cache.")
                return response

        try:
            response = super().request(method, url, headers, params, data, json)
        except Exception as e:
            print(response)
            raise e

        if self.cache:
            set_cache(key, response)
        print("ok.")

        return response


# End

ChapterRange = namedtuple("ChapterRange", "start end")


def parse_novel(source: Source, url: str, chapter_range: Optional[ChapterRange]):
    novel = source.novel(url)
    pprint(novel)

    if chapter_range is not None:
        flat = [chapter for volume in novel.volumes for chapter in volume.chapters]
        for chapter in flat[chapter_range.start : chapter_range.end]:
            source.chapter(chapter)
            pprint(chapter)


def parse_metadata(source: MetaSource, url: str):
    metadata = source.retrieve(url)
    pprint(metadata)


def parse(url: str, chapter_range: Optional[ChapterRange], gateway: BaseHttpGateway):

    try:
        parse_novel(locate_novel_source(url)(gateway), url, chapter_range)
        return
    except UnknownSourceException:
        pass

    try:
        parse_metadata(locate_metadata_source(url)(gateway), url)
        return
    except UnknownSourceException:
        pass

    print("Error: The url provided does not match any available source.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="The website url to parse.")
    parser.add_argument("-r", "--range", help="Range of chapters to download.")
    parser.add_argument("--no-cache", action="store_true", help="Disable cache usage.")
    args = parser.parse_args()

    gateway = DebugGateway(cache=not args.no_cache)

    chapter_range = None
    if args.range is not None:
        start, end = args.range.split(":")
        chapter_range = ChapterRange(int(start), int(end))

    parse(args.url, chapter_range, gateway)
