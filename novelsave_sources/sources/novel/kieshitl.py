from typing import Tuple, List

from .source import Source
from ...models import Novel, Chapter, Metadata


class KieshiTl(Source):
    name = 'Kieshi\'s Little Steps'
    base_urls = ('https://kieshitl.wordpress.com',)

    def novel(self, url: str) -> Tuple[Novel, List[Chapter], List[Metadata]]:
        soup = self.soup(url)

        entry_content = soup.select_one('div.entry-content')

        author = ''
        for p in entry_content.find_all('p'):
            text: str = p.text
            if text.startswith('Author:'):
                author = text.replace('Author:', '')
                break

        novel = Novel(
            title=soup.select_one('h1.page-title').text.strip(),
            author=author,
            thumbnail_url=entry_content.find('img')['src'],
            url=url
        )

        chapters = []
        for i, a in enumerate(soup.select('.entry-content > ul a')):
            chapter = Chapter(
                index=i,
                url=a['href']
            )

            chapters.append(chapter)

        return novel, chapters, []

    def chapter(self, chapter: Chapter):
        soup = self.soup(chapter.url)

        _, no = soup.select_one('h1.entry-title').text.split('Chapter', maxsplit=1)

        chapter.title = soup.select_one('.entry-content > h2').text.strip()
        chapter.paragraphs = []

        for p in soup.select('.entry-content > h2 ~ p.has-medium-font-size:not(.has-text-align-right):not('
                             '.has-pale-cyan-blue-background-color):not(.has-text-align-left)'):
            chapter.paragraphs.append(p.text.strip())
