import ssl
import warnings
from abc import ABC, abstractmethod

import cloudscraper
from requests import Response
from requests.cookies import RequestsCookieJar
from urllib3.exceptions import InsecureRequestWarning


class BaseHttpGateway(ABC):
    """Base gateway interface that defines http communication"""

    @abstractmethod
    def request(
        self,
        method: str,
        url: str,
        headers: dict = None,
        params: dict = None,
        data: dict = None,
        json: dict = None,
    ) -> Response:
        """Send an http request to the specified url using the specified options

        :param method: The method of request to send. ex: GET, POST, PUT
        :type method: str
        :param url: The endpoint to which the request to be made
        :type url: str
        :param headers: The headers to be send with the request.
            If not specified sends default headers from requests module.
        :type headers: dict
        :param params: The query parameters to be send with the request.
        :type params: dict
        :param data: 'x-www-form-urlencoded' to be send with the request.
        :type data: dict
        :param json: json to be sent in the request body.
        :type json: dict

        :return: The :class:`response <requests.Response>` resulting from
            the request
        :rtype: requests.Response
        """

    def get(self, *args, **kwargs):
        """Aliased method to send GET request using :meth:`request` method"""
        return self.request("GET", *args, **kwargs)

    def post(self, *args, **kwargs):
        """Aliased method to send POST request using :meth:`request` method"""
        return self.request("POST", *args, **kwargs)

    @property
    @abstractmethod
    def cookies(self) -> RequestsCookieJar:
        """Get current cookies being used in session

        The setter for this property must also be implemented.

        :return: The cookies in the session
        :rtype: RequestsCookieJar
        """

    @cookies.setter
    @abstractmethod
    def cookies(self, cookies: RequestsCookieJar):
        """Replace the existing cookies of the client with the provided"""


class DefaultHttpGateway(BaseHttpGateway):
    """Default Http gateway implementation used by sources

    This implementation has the following properties:

    - Uses cloudscraper package, which detects Cloudflare's anti-bot pages. ::

        self.session = cloudscraper.create_scraper(ssl_context=ctx)

    - Disables SSL protection, as this seems to break most sites. ::

        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        self.session = ... # initialize scraper session

        self.session.verify = False

      As such also disables :exc:`InsecureRequestWarning` in the request context. ::

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", InsecureRequestWarning)
            # logic
    """

    def __init__(self):
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        self.session = cloudscraper.create_scraper(
            ssl_context=ctx,
        )

        self.session.verify = False

    def request(
        self,
        method: str,
        url: str,
        headers: dict = None,
        params: dict = None,
        data: dict = None,
        json: dict = None,
    ) -> Response:

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", InsecureRequestWarning)
            return self.session.request(
                method, url, headers=headers, params=params, data=data, json=json
            )

    @property
    def cookies(self) -> RequestsCookieJar:
        return self.session.cookies

    @cookies.setter
    def cookies(self, cookies: RequestsCookieJar):
        self.session.cookies = cookies
