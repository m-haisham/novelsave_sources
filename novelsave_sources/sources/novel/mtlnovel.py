from typing import List, Tuple

from .source import Source
from ...models import Chapter, Novel, Metadata


class MtlNovel(Source):
    name = 'MTL Novel'
    base_urls = ('https://www.mtlnovel.com',)

    def novel(self, url: str) -> Tuple[Novel, List[Chapter], List[Metadata]]:
        soup = self.soup(url)

        author = ''
        info_element = soup.select_one('.info > tbody')
        for element in info_element.select('tr'):
            text = element.text
            if text.startswith('Author:'):
                author = text[7:]
                break
        
        novel = Novel(
            title=soup.select_one('.entry-title').text.strip(),
            author=author,
            thumbnail_url=soup.select_one('.main-tmb')['src'],
            url=url,
        )

        # chapter list
        chapter_list_url = '/'.join(s.strip('/') for s in (url, 'chapter-list')) + '/'
        soup = self.soup(chapter_list_url)

        chapters = []
        for i, a in enumerate(reversed(soup.select('.ch-list .ch-link'))):

            chapter = Chapter(
                index=i,
                title=a.text.strip(),
                url=a['href'],
            )

            chapters.append(chapter)

        return novel, chapters, []

    def chapter(self, chapter: Chapter):
        soup = self.soup(chapter.url)

        paragraphs = soup.select_one('.par')

        # remove ad frames
        for frame in paragraphs.select('amp-iframe'):
            frame.decompose()

        chapter.title = soup.select_one('.current-crumb').text.strip()
        chapter.paragraphs = str(paragraphs)
