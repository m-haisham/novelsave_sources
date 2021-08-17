from typing import Tuple, List

from .source import Source
from ...models import Novel, Chapter, Metadata


class RoyalRoad(Source):
    name = 'Royal Road'
    base_urls = ('https://www.royalroad.com',)

    def novel(self, url: str) -> Tuple[Novel, List[Chapter], List[Metadata]]:
        soup = self.soup(url)

        novel = Novel(
            title=soup.select_one('h1[property="name"]').text.strip(),
            author=soup.select_one('span[property="name"]').text.strip(),
            thumbnail_url=soup.select_one('.page-content-inner .thumbnail')['src'],
            synopsis=soup.select_one('.description > [property="description"]').text.strip(),
            url=url,
        )

        metadata = []
        for a in soup.select('a.label[href*="tag"]'):
            metadata.append(Metadata('subject', a.text.strip()))

        chapters = []
        for a in soup.find('tbody').findAll('a', href=True):
            chapter = Chapter(
                index=len(chapters),
                title=a.text.strip(),
                url=self.base_urls[0] + a["href"],
            )

            chapters.append(chapter)

        return novel, chapters, metadata

    def chapter(self, chapter: Chapter):
        soup = self.soup(chapter.url)

        contents = soup.select_one('.chapter-content')
        self.clean_contents(contents)

        chapter.title = soup.find('h1').text.strip()
        chapter.paragraphs = str(contents)
