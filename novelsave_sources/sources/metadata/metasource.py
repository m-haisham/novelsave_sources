from typing import List

import requests
from bs4 import BeautifulSoup

from ..crawler import Crawler
from ...models import MetaData


class MetaSource(Crawler):
    base_urls: List[str]

    @classmethod
    def of(cls, url: str):
        """
        :return: whether the url is from this source
        """
        return any([url.startswith(url) for url in cls.base_urls])

    def retrieve(self, url) -> List[MetaData]:
        """
        retrieves metadata from url

        :param url: metadata source
        :return: list of metadata
        """
        raise NotImplementedError
