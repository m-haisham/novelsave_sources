import datetime
from typing import List

import requests
from bs4 import BeautifulSoup
from requests.cookies import RequestsCookieJar

from ..exceptions import BadResponseException

headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko)'
                         ' Chrome/92.0.4515.159 Mobile Safari/537.36'}


class Crawler:
    lang: str
    base_urls: List[str]
    last_updated: datetime.date

    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {**self.session.headers, **headers}

    def set_cookies(self, cookies: RequestsCookieJar):
        self.session.cookies = cookies

    def get_soup(self, url: str) -> BeautifulSoup:
        """Download website html and create a bs4 object"""
        return BeautifulSoup(self.request_get(url).content, 'lxml')

    def request(self, method: str, url: str, **kwargs):
        """Create a request to the url and return the response if ok

        :raises BadResponseException: if the response is not valid (status_code==200)
        """
        response = self.session.request(method, url, **kwargs)
        if not response.ok:
            raise BadResponseException(
                response,
                'Bad Response {}'.format({'status_code': response.status_code, 'url': response.url})
            )

        return response

    def request_get(self, url, **kwargs):
        """Creates a get request to the specified url"""
        return self.request('GET', url, **kwargs)

