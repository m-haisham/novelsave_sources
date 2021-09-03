import re
from abc import ABC, abstractmethod
from typing import Tuple, Union
from urllib.parse import urlparse

from requests.cookies import RequestsCookieJar

from ..crawler import Crawler
from ...exceptions import UnavailableException
from ...models import Novel, Chapter


class Source(Crawler, ABC):
    name: str
    lang = 'en'
    login_viable: bool = False
    search_viable: bool = False

    @classmethod
    def of(cls, url: str) -> bool:
        """
        :param url: url to test
        :return: whether the url is from this source
        """
        return any(url.startswith(base_url) for base_url in cls.base_urls)

    def __init__(self):
        super(Source, self).__init__()

        # set default cookie domains
        if not hasattr(self, 'cookie_domains'):
            self.cookie_domains = []
            for url in self.base_urls:
                netloc = urlparse(url).netloc
                self.cookie_domains += [
                    netloc,
                    re.search(r'.+?(\..+)', netloc).group(1),  # remove the segment before first dot
                ]

    def login(self, email: str, password: str):
        """Login to the source and assign the required cookies"""
        raise UnavailableException(f"'{self.__name__}' scraper does not provide login functionality.")

    def search(self, keyword: str, *args, **kwargs):
        """Search for a novel on the source"""
        raise UnavailableException(f"'{self.__name__}' scraper does not provide search functionality.")

    def set_cookies(self, cookies: Union[RequestsCookieJar, Tuple[dict]]):
        """
        Replaces current cookiejar with given cookies

        :param cookies: new cookiejar
        """
        if type(cookies) == RequestsCookieJar:
            super(Source, self).set_cookies(cookies)
        elif type(cookies) == tuple:
            # clear preexisting cookies associated with source
            for domain in self.cookie_domains:
                try:
                    self.session.cookies.clear(domain=domain)
                except KeyError:
                    pass

            # add the dict formatted cookies
            for cookie in cookies:
                self.session.cookies.set(**cookie)
        else:
            raise TypeError(
                f"Unexpected type received: {type(cookies)}; Require either 'RequestsCookieJar' or 'Tuple[dict]'")

    @abstractmethod
    def novel(self, url: str) -> Novel:
        """Download and parse novel information

        :param url: link to novel profile
        :return: novel object containing volumes and metadata
        """
        raise NotImplementedError

    @abstractmethod
    def chapter(self, chapter: Chapter):
        """Download and parse chapter content

        Replaces the existing chapter's paragraphs attribute
        """
        raise NotImplementedError
