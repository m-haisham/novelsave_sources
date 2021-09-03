import datetime
from typing import List, Tuple

from .source import Source
from ...models import Chapter, Volume, Novel, Metadata


class NovelGate(Source):
    base_urls = ('https://novelgate.net',)
    last_updated = datetime.date(2021, 9, 3)

    def novel(self, url: str) -> Novel:
        soup = self.get_soup(url.rstrip('/') + '/')

        film_content = soup.select_one('.film-content')
        for element in film_content.select('h3, .tags'):
            element.extract()

        novel = Novel(
            title=soup.select_one('.film-info .name').text.strip(),
            author=soup.select_one('a[href*="author"]').text.strip(),
            thumbnail_url=soup.select_one('.film-info .book-cover')['data-original'],
            synopsis=[p.strip() for p in film_content.find_all(text=True, recursive=True) if p.strip()],
            url=url,
        )

        for a in soup.select('.film-info a[href*="genre"]'):
            novel.metadata.append(Metadata('subject', a.text.strip()))

        chapter_count = 0
        for i, div in enumerate(soup.select('#list-chapters > .book')):
            volume = Volume(i, div.select_one('.title a').text.strip())

            for a in div.select('.list-chapters > li a'):
                chapter = Chapter(
                    index=chapter_count,
                    title=a.text.strip(),
                    url=self.base_urls[0] + a['href'],
                )

                chapter_count += 1
                volume.chapters.append(chapter)

            novel.volumes.append(volume)

        return novel

    def chapter(self, chapter: Chapter):
        soup = self.get_soup(chapter.url)

        contents = soup.select_one('#chapter-body')
        self.clean_contents(contents)

        for element in contents.select('.language'):
            element.extract()

        chapter.paragraphs = str(contents)
