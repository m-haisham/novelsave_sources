from typing import List

from ..crawler import Crawler
from ...models import Metadata


class MetaSource(Crawler):
    lang = 'en'

    @classmethod
    def of(cls, url: str):
        """
        :return: whether the url is from this source
        """
        return any([url.startswith(base_url) for base_url in cls.base_urls])

    def retrieve(self, url) -> List[Metadata]:
        """
        retrieves metadata from url

        :param url: metadata source
        :return: list of metadata
        """
        raise NotImplementedError
