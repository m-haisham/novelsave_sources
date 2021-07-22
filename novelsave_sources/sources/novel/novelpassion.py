from typing import List, Tuple

from .source import Source
from ...models import Chapter, Novel


class NovelPassion(Source):
    base_urls = ['https://www.novelpassion.com']

    def novel(self, url: str) -> Tuple[Novel, List[Chapter]]:
        soup = self.soup(url)

        authors = [a.text.strip() for a in soup.select('.dns .stq[href*="author"]')]
        synopsis_paragraphs = [p.text.strip() for p in soup.select('.j_synopsis p')]

        novel = Novel(
            title=soup.select_one('.psn h2.ddm').text.strip(),
            author=', '.join(authors),
            thumbnail=self.base_urls[0] + soup.select_one('.g_thumb img')['src'],
            synopsis='\n'.join(synopsis_paragraphs),
            url=url,
        )

        for a in soup.select('.dns .stq[href*="category"]'):
            novel.add_meta('subject', a.text.strip())

        chapters = []
        for i, a in enumerate(reversed(soup.select('.content-list a'))):
            chapter = Chapter(
                index=i,
                title=a.select_one('span').text.strip(),
                url=self.base_urls[0] + a['href'],
            )

            chapters.append(chapter)

        return novel, chapters

    def chapter(self, chapter: Chapter):
        soup = self.soup(chapter.url)

        content = soup.select_one('.cha-words')
        self.clean_contents(content)

        chapter.title = soup.select_one('h2.dac').text.strip()
        chapter.paragraphs = str(content)
