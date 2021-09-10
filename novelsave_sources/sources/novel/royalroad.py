import datetime

from .source import Source
from ...models import Novel, Chapter, Metadata


class RoyalRoad(Source):
    name = 'Royal Road'
    base_urls = ('https://www.royalroad.com',)
    last_updated = datetime.date(2021, 9, 6)

    def novel(self, url: str) -> Novel:
        soup = self.get_soup(url)

        novel = Novel(
            title=soup.select_one('h1[property="name"]').text.strip(),
            author=soup.select_one('span[property="name"]').text.strip(),
            thumbnail_url=soup.select_one('.page-content-inner .thumbnail')['src'],
            synopsis=[p.text.strip() for p in soup.select('.description > [property="description"] > p')],
            url=url,
        )

        for a in soup.select('a.label[href*="tag"]'):
            novel.metadata.append(Metadata('subject', a.text.strip()))

        volume = novel.get_default_volume()
        for a in soup.find('tbody').findAll('a', href=True):
            chapter = Chapter(
                index=len(volume.chapters),
                title=a.text.strip(),
                url=self.base_urls[0] + a["href"],
            )

            volume.chapters.append(chapter)

        return novel

    def chapter(self, chapter: Chapter):
        soup = self.get_soup(chapter.url)

        contents = soup.select_one('.chapter-content')
        self.clean_contents(contents)

        chapter.title = soup.find('h1').text.strip()
        chapter.paragraphs = str(contents)
