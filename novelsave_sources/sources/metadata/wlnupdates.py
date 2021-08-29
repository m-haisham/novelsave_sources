import datetime
from typing import List

import requests

from .metasource import MetaSource
from ...models import Metadata


class WlnUpdates(MetaSource):
    base_urls = ('https://www.wlnupdates.com/',)
    last_updated = datetime.date(2021, 8, 25)

    api_endpoint = 'https://www.wlnupdates.com/api'

    def retrieve(self, url) -> List[Metadata]:
        metadata = []
        
        # get json data
        id = int(url.split('/')[4])
        data = self.api_request(id, 'get-series-id')['data']

        # alternate names
        for name in data['alternatenames']:
            if name == data['title']:
                continue

            metadata.append(Metadata('title', name, others={'type': 'alternate'}))

        # illustrators
        for obj in data['illustrators']:
            metadata.append(Metadata('contributor', obj['illustrator'], others={'role': 'ill'}))

        # publishers
        for obj in data['publishers']:
            metadata.append(Metadata('publisher', obj['publisher']))

        # genre
        for obj in data['genres']:
            metadata.append(Metadata('subject', obj['genre']))

        # tags
        for obj in data['tags']:
            metadata.append(Metadata('tag', obj['tag']))

        # original language
        if data['orig_lang']:
            metadata.append(Metadata('lang', data['orig_lang'], others={'id_': 'original language'}))

        # publication
        if data['pub_date']:
            metadata.append(Metadata('date', data['pub_date'], others={'role': 'publication'}))

        return metadata

    def api_request(self, id: int, mode: str):
        return self.session.post(self.api_endpoint, json={'id': id, 'mode': mode}).json()
