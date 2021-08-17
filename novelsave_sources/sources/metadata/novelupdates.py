from typing import List

from .metasource import MetaSource
from ...models import Metadata


class NovelUpdates(MetaSource):
    base_urls = ('https://www.novelupdates.com',)

    def retrieve(self, url) -> List[Metadata]:
        metadata = []
        soup = self.soup(url)

        # alternate titles
        for text in soup.select_one('#editassociated').find_all(text=True, recursive=False):
            metadata.append(Metadata('title', text.strip(), {'type': 'alternate'}))

        # novel type
        metadata.append(Metadata('type', soup.select_one('.genre.type').text))

        # genre
        for a in soup.select('#seriesgenre > a'):
            metadata.append(Metadata('subject', a.text))

        # og language
        metadata.append(Metadata('lang', soup.select_one('#showlang > a').text, {'id_': 'original language'}))

        # illustrators
        for a in soup.select('#showartists > a'):
            metadata.append(Metadata('contributor', a.text, {'role': 'ill'}))

        # publishers
        if soup.select_one('#showopublisher > a'):
            metadata.append(Metadata('publisher', soup.select_one('#showopublisher > a').text, {'role': 'original'}))
        if soup.select_one('#showepublisher > a'):
            metadata.append(Metadata('publisher', soup.select_one('#showepublisher > a').text, {'role': 'english'}))

        # publication
        if not soup.select_one('#edityear > .seriesna'):
            metadata.append(Metadata('date', soup.select_one('#edityear').text.strip(), {'role': 'publication'}))

        return metadata
