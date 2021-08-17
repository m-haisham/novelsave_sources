import select
from typing import List, Tuple

import requests
from bs4 import BeautifulSoup

from .source import Source
from ...models import Chapter, Novel, Metadata


class ScribbleHub(Source):
    name = 'Scribble Hub'
    base_urls = ('https://www.scribblehub.com',)

    def novel(self, url: str) -> Tuple[Novel, List[Chapter], List[Metadata]]:
        soup = self.soup(url)

        novel = Novel(
            title=soup.select_one('div.fic_title').text.strip(),
            author=soup.select_one('span.auth_name_fic').text.strip(),
            synopsis=soup.select_one('.wi_fic_desc').text.strip(),
            thumbnail_url=soup.select_one('.fic_image img')['src'],
            url=url,
        )

        metadata = []
        for a in soup.select('a.fic_genre'):
            metadata.append(Metadata('subject', a.text.strip()))

        for a in soup.select('a.stag'):
            metadata.append(Metadata('tag', a.text.strip()))

        id_ = int(url.split('/')[4])
        chapters = self.parse_toc(id_)

        return novel, chapters, metadata

    def chapter(self, chapter: Chapter):
        soup = self.soup(chapter.url)

        chapter.title = soup.select_one('.chapter-title').text.strip()
        chapter.paragraphs = str(soup.select_one('#chp_raw'))

    def parse_toc(self, id_: int) -> List[Chapter]:
        response = requests.post(
            'https://www.scribblehub.com/wp-admin/admin-ajax.php',
            data={
                'action': 'wi_gettocchp',
                'strSID': id_,
            },
        )

        soup = BeautifulSoup(response.content, 'lxml')

        chapters = []
        for i, a in enumerate(reversed(soup.select('li > a'))):
            chapter = Chapter(
                index=i,
                title=a.text.strip(),
                url=a['href']
            )

            chapters.append(chapter)

        return chapters
