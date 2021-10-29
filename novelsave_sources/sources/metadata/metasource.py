from abc import abstractmethod
from typing import List

from ..crawler import Crawler
from ...models import Metadata


class MetaSource(Crawler):
    lang = 'en'

    @classmethod
    def of(cls, url: str):
        """Checks whether the url is from this source"""
        return any(url.startswith(base_url) for base_url in cls.base_urls)

    @abstractmethod
    def retrieve(self, url: str) -> List[Metadata]:
        """Retrieves metadata from url"""

