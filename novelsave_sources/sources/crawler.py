from typing import List, Dict

import requests
from bs4 import BeautifulSoup
from requests.cookies import RequestsCookieJar

from ..exceptions import BadResponseException

headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko)'
                         ' Chrome/92.0.4515.159 Mobile Safari/537.36'}


class Crawler:
    retry_count = 5

    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {**self.session.headers, **headers}

    def set_cookies(self, cookies: RequestsCookieJar):
        self.session.cookies = cookies

    def soup(self, url: str) -> BeautifulSoup:
        """
        Download website html and create a bs4 object

        :param url: website to be downloaded
        :return: created bs4 object
        """
        response = self.request_get(url)
        return BeautifulSoup(response.content, 'lxml')

    def request_get(self, url, _tries=0, **kwargs):
        # limiting retry requests
        if _tries >= self.retry_count:
            return

        # request
        response = self.session.get(url, **kwargs)
        if response.ok:
            return response

        raise BadResponseException(response, f'{response.status_code}: {response.url}')

