import re
from typing import Tuple, List, Union
from urllib.parse import urlparse

from bs4 import Comment
from requests.cookies import RequestsCookieJar

from ...exceptions import UnavailableException
from ...utils import slugify
from ...models import Novel, Chapter
from ..crawler import Crawler


class Source(Crawler):
    __name__: str
    __login__: bool = False
    __search__: bool = False

    base_urls: List[str]

    cookie_domains = []

    @classmethod
    def of(cls, url: str) -> bool:
        """
        :param url: url to test
        :return: whether the url is from this source
        """
        return any([url.startswith(url) for url in cls.base_urls])

    def __init__(self):
        super(Source, self).__init__()

        # set default cookie domains
        if not self.cookie_domains:
            for url in self.base_urls:
                netloc = urlparse(url).netloc
                self.cookie_domains = [
                    netloc,
                    re.search(r'.+?(\..+)', netloc).group(1),  # remove the segment before first dot
                ]

    def login(self, email: str, password: str):
        """Login to the source and assign the required cookies"""
        raise UnavailableException(f'{self.__name__} scraper does not provide login functionality.')

    def search(self, keyword: str, *args, **kwargs):
        """Search for a novel on the source"""
        raise UnavailableException(f'{self.__name__} scraper does not provide search functionality.')

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

    def novel(self, url: str) -> Tuple[Novel, List[Chapter]]:
        """
        soup novel information from url

        :param url: link pointing to novel
        :return: novel, table of content (chapters with only field no, title and url), and volumes
        """
        raise NotImplementedError

    def chapter(self, url: str) -> Chapter:
        """
        soup chapter information from url

        :param url: link pointing to chapter
        :return: chapter object
        """
        raise NotImplementedError

    def novel_folder_name(self, url):
        """
        :param url: novel url
        :return: suitable novel folder name
        """
        return slugify(url.strip('/ ').split('/')[-1])

    # ---- Inspired from https://github.com/dipu-bd/lightnovel-crawler ----
    # ----      And almost a perfect copy of the functions below       ----

    bad_tags = [
        'noscript', 'script', 'iframe', 'form', 'hr', 'img', 'ins',
        'button', 'input', 'amp-auto-ads', 'pirate'
    ]

    blacklist_patterns = [
        r'^[\W\D]*(volume|chapter)[\W\D]+\d+[\W\D]*$',
    ]

    def is_blacklisted(self, text):
        """
        :return: whether the text is black listed
        """
        for pattern in self.blacklist_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True

        return False

    def clean_contents(self, contents):
        if not contents:
            return contents

        contents.attrs = {}
        for element in contents.find_all(True):
            self.clean_element(element)

        return contents

    def clean_element(self, element):
        # remove comments
        if isinstance(element, Comment):
            element.extract()

        elif element.name == 'br':
            next_element = getattr(element, 'next_sibling')
            if next_element and next_element.name == 'br':
                element.extract()

        # Remove bad tags
        elif element.name in self.bad_tags:
            element.extract()

        # Remove empty elements
        elif not element.text.strip():
            element.extract()

        # Remove blacklisted elements
        elif self.is_blacklisted(element.text):
            element.extract()

        # Remove attributes
        elif hasattr(element, 'attrs'):

            # preserve href attribute of <a>
            if element.name == 'a':
                element.attrs = {'href': element.get('href') or '#'}
            else:
                element.attrs = {}
