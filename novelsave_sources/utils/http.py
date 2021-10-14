import ssl
from abc import ABC, abstractmethod

import cloudscraper
from requests import Response
from requests.cookies import RequestsCookieJar


class BaseHttpGateway(ABC):
    """Base gateway interface that defines http communication"""

    @abstractmethod
    def request(self, method: str, url: str, headers: dict = None, params: dict = None, data: dict = None,
                json: dict = None) -> Response:
        """Send an http request to the specified url using the specified method"""

    def get(self, *args, **kwargs):
        """Aliased method to send GET request using :request method"""
        return self.request(*args, method='GET', **kwargs)

    def post(self, *args, **kwargs):
        """Aliased method to send POST request using :request method"""
        return self.request(*args, method='POST', **kwargs)

    @property
    @abstractmethod
    def cookies(self) -> RequestsCookieJar:
        """Get current cookies being used in session"""

    @cookies.setter
    @abstractmethod
    def cookies(self, cookies: RequestsCookieJar):
        """Replace the existing cookies of the client with the provided"""


class CloudScraperHttpGateway(BaseHttpGateway):
    """Http gateway implementation that uses cloudscraper module for http requests"""

    def __init__(self):
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        self.session = cloudscraper.create_scraper(
            ssl_context=ctx,
        )

    def request(self, method: str, url: str, headers: dict = None, params: dict = None, data: dict = None,
                json: dict = None) -> Response:
        return self.session.request(method, url, headers=headers, params=params, data=data, json=json)

    @property
    def cookies(self) -> RequestsCookieJar:
        return self.session.cookies

    @cookies.setter
    def cookies(self, cookies: RequestsCookieJar):
        self.session.cookies = cookies
