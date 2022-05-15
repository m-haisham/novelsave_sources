import datetime
import re
from abc import ABC
from typing import List, Union, Optional
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup, Comment
from requests.cookies import RequestsCookieJar

from ..exceptions import BadResponseException
from ..utils.gateways import BaseHttpGateway, DefaultHttpGateway


class Crawler(ABC):
    """Base crawler class

    Implements crawler specific helper methods that can be used
    when parsing html content

    Attributes:
        lang (str): The language of the content available through the source.
            It is specified ``multi`` if the source supports multiple languages.

        base_urls (List[str]): The hostnames of the websites that this crawler
            supports.

        last_updated (datetime.date): The date at which the specific crawler
            implementation was last updated.

        bad_tags (List[str]): List of names of tags that should be removed from
            chapter content for this specific crawler.

        blacklist_patterns (List[str]): List of regex patterns denoting text that
            should be removed from chapter content.

        notext_tags (List[str]): List of names of tags that even if there is no
            text should not be removed from chapter content.

            Elements with no text are usually removed from the chapter content,
            unless the element is specified in this list.

        preserve_attrs (List[str]): Element attributes that contain meaningful content
            and should be kept with in the element during attribute cleanup.
    """

    lang: str
    base_urls: List[str]
    last_updated: datetime.date

    @classmethod
    def of(cls, url: str) -> bool:
        """Check whether the url is from the this source

        The source implementations may override this method to provide
        custom matching functionality.

        The default implementation checks if the hostname of the
        url matches any of the base urls of the source.

        :param url: The url to test if it belongs to this source
        :type url: str

        :return: Whether the url is from this source
        :rtype: bool
        """
        return any(url.startswith(base_url) for base_url in cls.base_urls)

    def __init__(self, http_gateway: BaseHttpGateway = None):
        self.http_gateway = (
            http_gateway if http_gateway is not None else DefaultHttpGateway()
        )

        self.init()

    def init(self):
        """Call this method instead of __init__ for trivial purposes

        The purpose can be any of:

        - editing bad_tags or blacklist_patterns
        """

    def set_cookies(self, cookies: RequestsCookieJar):
        self.http_gateway.cookies = cookies

    def get_soup(self, url: str, method: str = "GET", **kwargs) -> BeautifulSoup:
        """Makes a request to the url and attempts to make a :class:`BeautifulSoup`
        object from the response content.

        Once the response is acquired, soup object is created using :meth:`~novelsave_sources.sources.Crawler.make_soup`.
        Then the soup object is checked for the ``body`` to check if document was
        retrieved successfully.

        :param url: forwarded to :meth:`~novelsave_sources.sources.Crawler.request`
        :type url: str

        :param method: forwarded to :meth:`~novelsave_sources.sources.Crawler.request`
        :type method: str

        :param kwargs: forwarded to :meth:`~novelsave_sources.sources.Crawler.request`

        :return: The created soup object
        :rtype: BeautifulSoup

        :raises ConnectionError: If document was not retrieved successfully
        """
        soup = self.make_soup(self.request(method, url, **kwargs).content, "lxml")
        if not soup.find("body"):
            raise ConnectionError("HTML document was not loaded correctly.")

        return soup

    @staticmethod
    def make_soup(text: Union[str, bytes], parser: str = "lxml") -> BeautifulSoup:
        """Create a new soup object using the specified parser

        :param text: The content for the soup
        :type text: str | bytes

        :param parser: The html tree parser to use (default = 'lxml')
        :type parser: str

        :return: The created soup object
        :rtype: BeautifulSoup
        """
        return BeautifulSoup(text, parser)

    def request(self, method: str, url: str, **kwargs) -> requests.Response:
        """Send a request to the provided url using the specified method

        Checks if the response is valid before returning, if its not valid
        throws an exception.

        :param method: Request method ex: GET, POST, PUT
        :type method: str

        :param url: The url endpoint to make the request to
        :type url: str

        :param kwargs: Forwarded to
            :meth:`http_gateway.request <novelsave_sources.utils.gateways.BaseHttpGateway.request>`

        :return: The response from the request
        :rtype: requests.Response

        :raises BadResponseException: if the response is not valid (status code != 200)
        """
        response = self.http_gateway.request(method, url, **kwargs)
        if not response.ok:
            raise BadResponseException(response)

        return response

    def request_get(self, url, **kwargs):
        """Creates a get request to the specified url"""
        return self.request("GET", url, **kwargs)

    # ---- Inspired from https://github.com/dipu-bd/lightnovel-crawler ----
    # ----      And almost a perfect copy of the functions below       ----

    bad_tags = [
        "noscript",
        "script",
        "style",
        "iframe",
        "ins",
        "header",
        "footer",
        "button",
        "input",
        "amp-auto-ads",
        "pirate",
        "figcaption",
        "address",
        "tfoot",
        "object",
        "video",
        "audio",
        "source",
        "nav",
        "output",
        "select",
        "textarea",
        "form",
        "map",
    ]

    blacklist_patterns = []

    notext_tags = [
        "img",
    ]

    preserve_attrs = [
        "href",
        "src",
        "alt",
    ]

    def is_blacklisted(self, text):
        """Whether the text is blacklisted"""
        return any(
            re.search(pattern, text, re.IGNORECASE)
            for pattern in self.blacklist_patterns
        )

    def clean_contents(self, contents):
        """Remove unnecessary elements and attributes"""
        if not contents:
            return contents

        contents.attrs = {}
        for element in contents.find_all(True):
            self.clean_element(element)

        return contents

    def clean_element(self, element):
        """
        If the element does not add any meaningful content the element
        is removed, this can happen on either of below conditions.

        - Element is a comment
        - Element is a <br> and the next sibling element is also a <br>
        - Element is part of the bad tags (undesired tags that dont add content)
        - The element has no text and has no children and is not part of notext_tags
          (elements that doesnt need text to be meaningful)
        - The text of the element matches one of the blacklisted patterns
          (undesirable text such as ads and watermarks)

        If none of the conditions are met, all the attributes except those marked
        important :attr:`preserve_attrs` are removed from this element
        """
        # remove comments
        if isinstance(element, Comment):
            element.extract()

        elif element.name == "br":
            next_element = getattr(element, "next_sibling")
            if next_element and next_element.name == "br":
                element.extract()

        # Remove bad tags
        elif element.name in self.bad_tags:
            element.extract()

        # Remove empty elements
        elif not element.text.strip():
            if element.name not in self.notext_tags and not element.find_all(
                recursive=False
            ):
                element.extract()

        # Remove blacklisted elements
        elif self.is_blacklisted(element.text):
            element.extract()

        # Remove attributes
        elif hasattr(element, "attrs"):
            element.attrs = {
                key: element.get(key)
                for key in self.preserve_attrs
                if key in element.attrs
            }

    @staticmethod
    def find_paragraphs(element, **kwargs) -> List[str]:
        """Extract all text of the element into paragraphs"""
        paragraphs = []
        for t in element.find_all(text=True, **kwargs):
            text = str(t).strip()
            if not text:
                continue

            paragraphs.append(text)

        return paragraphs

    def to_absolute_url(self, url: str, current_url: Optional[str] = None) -> str:
        """Detects the url state and converts it into the appropriate absolute url

        There are several relevant states the url could be in:

        - absolute: starts with either 'https://' or 'http://', in this the url
          is returned as it without any changes.

        - missing schema: schema is missing and the url starts with '//', in this
          case the appropriate schema from either current url or base url is prefixed.

        - relative absolute: the url is relative to the website and starts with '/', in
          this case the base website location (netloc) is prefixed to the url:

        - relative current: the url is relative to the current webpage and does not match
          any of the above conditions, in this case the url is added to the current url provided.

        :param url: The url to be converted
        :type url: str

        :param current_url: The webpage from which the url is extracted
        :type current_url: Optional[str]

        :return: The absolute converted url
        :rtype: str
        """
        if url.startswith("http://") or url.startswith("https://"):
            return url
        if url.startswith("//"):
            return f"{urlparse(current_url or self.base_urls[0]).scheme}:{url}"
        elif url.startswith("/"):
            return self.base_urls[0].rstrip("/") + url

        return current_url.rstrip("/") + url
