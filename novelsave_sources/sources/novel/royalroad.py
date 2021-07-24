from typing import Tuple, List

from .source import Source
from ...models import Novel, Chapter


class RoyalRoad(Source):
    __name__ = 'Royal Road'
    base_urls = ['https://www.royalroad.com']

    def novel(self, url: str) -> Tuple[Novel, List[Chapter]]:
        soup = self.soup(url)

        novel = Novel(
            title=soup.find("h1", {"property": "name"}).text.strip(),
            thumbnail_url=soup.find("img", {"class": "img-offset thumbnail_url inline-block"})['src'],
            author=soup.find("span", {"property": "name"}).text.strip(),
            url=url,
        )

        chapters = []
        for a in soup.find('tbody').findAll('a', href=True):
            chapter = Chapter(
                index=len(chapters),
                title=a.text.strip(),
                url=self.base_urls[0] + a["href"],
            )

            chapters.append(chapter)

        return novel, chapters

    def chapter(self, chapter: Chapter):
        soup = self.soup(chapter.url)

        contents = soup.select_one('.chapter-content')
        self.clean_contents(contents)

        chapter.title = soup.find('h1').text.strip()
        chapter.paragraphs = str(contents)
