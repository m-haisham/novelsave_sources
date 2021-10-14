import datetime
import re
from abc import ABC
from typing import List, Union
from urllib.parse import urlparse

from bs4 import BeautifulSoup, Comment
from requests.cookies import RequestsCookieJar

from ..exceptions import BadResponseException
from ..utils.http import BaseHttpGateway, CloudScraperHttpGateway


class Crawler(ABC):
    lang: str
    base_urls: List[str]
    last_updated: datetime.date
    rejected: str

    def __init__(self, http_gateway: BaseHttpGateway = None):
        self.http_gateway = http_gateway if http_gateway is not None else CloudScraperHttpGateway()

    def set_cookies(self, cookies: RequestsCookieJar):
        self.http_gateway.cookies = cookies

    def get_soup(self, url: str, method: str = 'GET', **kwargs) -> BeautifulSoup:
        """Download website html and create a bs4 object"""
        soup = self.make_soup(self.request(method, url, **kwargs).content, 'lxml')
        if not soup.find('body'):
            raise ConnectionError('HTML document was not loaded correctly.')

        return soup

    @staticmethod
    def make_soup(text: Union[str, bytes], parser: str = 'lxml'):
        return BeautifulSoup(text, parser)

    def request(self, method: str, url: str, **kwargs):
        """Create a request to the url and return the response if ok

        :raises BadResponseException: if the response is not valid (status_code==200)
        """
        response = self.http_gateway.request(method, url, **kwargs)
        if not response.ok:
            raise BadResponseException(response)

        return response

    def request_get(self, url, **kwargs):
        """Creates a get request to the specified url"""
        return self.request('GET', url, **kwargs)

    # ---- Inspired from https://github.com/dipu-bd/lightnovel-crawler ----
    # ----      And almost a perfect copy of the functions below       ----

    bad_tags = [
        'noscript', 'script', 'style', 'iframe', 'ins', 'header', 'footer',
        'button', 'input', 'amp-auto-ads', 'pirate', 'figcaption', 'address',
        'tfoot', 'object', 'video', 'audio', 'source', 'nav', 'output', 'select',
        'textarea', 'form', 'map',
    ]

    blacklist_patterns = []

    notext_tags = [
        'img',
    ]

    preserve_attrs = [
        'href', 'src', 'alt',
    ]

    def is_blacklisted(self, text):
        """
        :return: whether the text is black listed
        """
        return any(
            re.search(pattern, text, re.IGNORECASE)
            for pattern in self.blacklist_patterns
        )

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
            if element.name not in self.notext_tags and not element.find_all(recursive=False):
                element.extract()

        # Remove blacklisted elements
        elif self.is_blacklisted(element.text):
            element.extract()

        # Remove attributes
        elif hasattr(element, 'attrs'):
            element.attrs = {key: element.get(key) for key in self.preserve_attrs if key in element.attrs}

    @staticmethod
    def find_paragraphs(element, **kwargs) -> List[str]:
        paragraphs = []
        for t in element.find_all(text=True, **kwargs):
            text = str(t).strip()
            if not text:
                continue

            paragraphs.append(text)

        return paragraphs

    def to_absolute_url(self, url: str, current_url: str = None) -> str:
        if url.startswith('http://') or url.startswith('https://'):
            return url
        if url.startswith('//'):
            return f'{urlparse(current_url or self.base_urls[0]).scheme}:{url}'
        elif url.startswith('/'):
            return self.base_urls[0].rstrip('/') + url

        return current_url.rstrip('/') + url
