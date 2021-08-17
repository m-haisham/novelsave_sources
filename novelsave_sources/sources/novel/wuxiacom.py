from typing import List, Tuple

from .source import Source
from ...models import Chapter, Novel, Metadata


class WuxiaCom(Source):
    name = 'WuxiaWorld.com'
    base_urls = ('https://www.wuxiaworld.com',)

    blacklist_patterns = [
        r'^<span>(...|\u2026)</span>$',
        r'^translat(ed by|or)',
        r'(volume|chapter) .?\d+',
    ]

    def novel(self, url: str) -> Tuple[Novel, List[Chapter], List[Metadata]]:
        soup = self.soup(url)

        authors = ''
        for d in soup.select_one('.media-body dl, .novel-body').select('dt, dd'):
            authors += d.text.strip()
            authors += ' ' if d.name == 'dt' else '; '

        novel = Novel(
            title=soup.select_one('.section-content h2').text,
            thumbnail_url=soup.select_one('img.media-object').get('src'),
            author=authors.strip().strip(';'),
            url=url,
        )

        chapters = []
        for panel in soup.select('#accordion .panel-default'):
            for a in panel.select('ul.list-chapters li.chapter-item a'):
                chapter = Chapter(
                    index=len(chapters),
                    url=self.base_urls[0] + a['href'],
                )

                chapters.append(chapter)

        return novel, chapters, []

    def chapter(self, chapter: Chapter):
        soup = self.soup(chapter.url)

        contents = soup.select_one('#chapterContent')
        if not contents:
            contents = soup.select_one('#chapter-content')
        if not contents:
            contents = soup.select_one('.panel-default .fr-view')
        if not contents:
            raise ValueError(f'Unable to read chapter content from {chapter}')

        for nav in (contents.select('.chapter-nav') or []):
            nav.extract()

        self.clean_contents(contents)

        chapter.title = soup.select_one('#chapter-outer  h4').text.strip()
        chapter.paragraphs = str(contents)
