import requests
from bs4 import BeautifulSoup
from requests.cookies import RequestsCookieJar
from typing import List, Dict, Set

from ..exceptions import BadResponseException

header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/39.0.2171.95 Safari/537.36'}


class Crawler:
    retry_count = 5

    def __init__(self):
        self.session = requests.Session()

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
        response = self.session.get(url, headers=header, **kwargs)
        if response.status_code == 200:  # ok
            return response

        raise BadResponseException(response, f'{response.status_code}: {response.url}')

    # ---- url parser ----

    def parse_query(self, query: str) -> Dict[str, List[str]]:
        parts = query.split('&')
        params = {}

        for part in parts:
            name, raw_value = part.split('=', maxsplit=1)
            values = set(raw_value.split(','))

            try:
                params[name] = params[name].union(values)
            except KeyError:
                params[name] = values

        return {key: list(value) for key, value in params.items()}
