from abc import abstractmethod
from typing import List

from ..crawler import Crawler
from ...models import Metadata


class MetaSource(Crawler):
    """MetaData source interface

    All metadata sources must implement this interface.
    """

    lang = "en"

    def __init__(self, *args, **kwargs):
        super(MetaSource, self).__init__(*args, **kwargs)

    @abstractmethod
    def retrieve(self, url: str) -> List[Metadata]:
        """Retrieves metadata from url

        An implementation might retrieve the metadata by requesting
        from an api endpoint or from scraping a website.

        :param url: Url pointing to the metadata
        :type url: str

        :return: List of metadata retrieved for the page.
        :rtype: List[Metadata]
        """
