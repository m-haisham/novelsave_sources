import argparse
import hashlib
from datetime import datetime, timedelta
import pickle
from typing import Optional
from requests import Response
from pathlib import Path
from novelsave_sources import locate_novel_source, locate_metadata_source
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
        print(f"{method.upper():4} {url} {flags}... ", end="")

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


def parse_novel(source: Source, url: str):
    novel = source.novel(url)
    pprint(novel)


def parse_metadata(source: MetaSource, url: str):
    pass


def parse(url: str, gateway: BaseHttpGateway):
    novel_source = locate_novel_source(url)
    if novel_source is not None:
        parse_novel(novel_source(gateway), url)
        return

    metadata_source = locate_metadata_source(url)
    if metadata_source is not None:
        parse_metadata(metadata_source(gateway), url)
        return

    print("Error: The url provided does not match any available source.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="The website url to parse.")
    parser.add_argument("--no-cache", action="store_true", help="Disable cache usage.")
    args = parser.parse_args()

    gateway = DebugGateway(cache=not args.no_cache)
    parse(args.url, gateway)
