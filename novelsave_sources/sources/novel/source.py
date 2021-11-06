import re
from abc import abstractmethod
from typing import List, Tuple, Union
from urllib.parse import urlparse

from requests.cookies import RequestsCookieJar

from ..crawler import Crawler
from ...exceptions import UnavailableException
from ...models import Chapter, Novel


class Source(Crawler):
    """Novel source interface

    All novel sources must implement this interface

    Attributes:
        name (Optional[str]): Alternative name for the source,
            otherwise use the class name ``Source.__name__`` magic attribute.

            For example::

                name = getattr(Source, 'name', Source.__name__)

        login_viable (bool): Specifies if the source has login functionality
            implemented.

        search_viable (bool): Specifies if the source has the ability to search for
            novels implemented.
    """

    name: str
    lang = "en"
    login_viable: bool = False
    search_viable: bool = False

    def __init__(self, *args, **kwargs):
        """
        When initializing the source,

        * The source is checked for cookie domains, if there are
          no cookie domains they are built using the :attr:`base_urls`.
        """
        super(Source, self).__init__(*args, **kwargs)

        # set default cookie domains
        if not hasattr(self, "cookie_domains"):
            self.cookie_domains = []
            for url in self.base_urls:
                netloc = urlparse(url).netloc
                self.cookie_domains += [
                    netloc,
                    re.search(r".+?(\..+)", netloc).group(
                        1
                    ),  # remove the segment before first dot
                ]

    def login(self, email: str, password: str):
        """Login to the source and assign the required cookies

        Even though unlike novel and chapter, login is not marked abstract
        it does not have an implementation. By default, it throws an
        :exc:`~novelsave_sources.UnavailableException`.

        You may specify whether login is implemented using
        :attr:`login_viable`.

        :param email: Email or username credentials
        :type email: str
        :param password: password credentials
        :type password: str
        """
        raise UnavailableException(
            f"'{type(self).__name__}' scraper does not provide login functionality."
        )

    def search(self, keyword: str, *args, **kwargs) -> List[Novel]:
        """Search for a novel on the source

        Even though unlike novel and chapter, search is not marked abstract
        it does not have an implementation. By default, it throws an
        :exc:`~novelsave_sources.UnavailableException`.

        You may specify whether search is implemented using
        :attr:`search_viable`.

        :param keyword: The query text to be used in the search. Usually
            part of title.
        :type keyword: str

        :return: The resulting novels from the search
        :rtype: List[Novel]
        """
        raise UnavailableException(
            f"'{type(self).__name__}' scraper does not provide search functionality."
        )

    def set_cookies(self, cookies: Union[RequestsCookieJar, Tuple[dict]]):
        """Replaces current cookiejar with given cookies

        This implementation supports multiple types of cookies.

        :param cookies: New cookies to be used
        :type cookies: Union[RequestsCookieJar, Tuple[dict]]

        :raises TypeError: If the cookies parameter does not match the
            expected type.
        """
        if type(cookies) == RequestsCookieJar:
            super(Source, self).set_cookies(cookies)
        elif type(cookies) == tuple:
            # clear preexisting cookies associated with source
            for domain in self.cookie_domains:
                try:
                    self.http_gateway.cookies.clear(domain=domain)
                except KeyError:
                    pass

            # add the dict formatted cookies
            for cookie in cookies:
                self.http_gateway.cookies.set(**cookie)
        else:
            raise TypeError(
                f"Unexpected type received: {type(cookies)}; Require either 'RequestsCookieJar' or 'Tuple[dict]'"
            )

    @abstractmethod
    def novel(self, url: str) -> Novel:
        """Download and parse novel information

        The typical implementation of this method is very straight forward.
        They download and parse the profile page into a novel object.
        Usually the table of contents would be a part of this. However,
        In the other instances, additional downloads may be required.

        :param url: The url pointing towards the main profile page
        :type url: str

        :return: Novel object that contains the parsed data
        :rtype: Novel
        """
        raise NotImplementedError

    @abstractmethod
    def chapter(self, chapter: Chapter):
        """Download and parse chapter content

        The typical implementation of this method retrieves the chapters
        reading content and updates the :attr:`~novelsave_sources.Chapter.paragraph`
        attribute of the provided chapter. It does not return any result.

        In rare instances, other attributes of the :class:`~novelsave_sources.Chapter`
        are also updated like :attr:`~novelsave_sources.Chapter.title`.

        :param chapter: Chapter object with atleast the :attr:`~novelsave_sources.Chapter.url`
            attribute option filled.
        :type chapter: Chapter
        """
        raise NotImplementedError
