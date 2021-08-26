from typing import List, Tuple

from .source import Source
from ...models import Chapter, Novel, Metadata


class NovelGate(Source):
    base_urls = ('https://novelgate.net',)

    def novel(self, url: str) -> Tuple[Novel, List[Chapter], List[Metadata]]:
        soup = self.soup(url.rstrip('/') + '/')

        film_content = soup.select_one('.film-content')
        for element in film_content.select('h3, .tags'):
            element.extract()

        novel = Novel(
            title=soup.select_one('.film-info .name').text.strip(),
            author=soup.select_one('a[href*="author"]').text.strip(),
            thumbnail_url=soup.select_one('.film-info .book-cover')['data-original'],
            synopsis='\n'.join([p.strip() for p in film_content.find_all(text=True, recursive=True) if p.strip()]),
            url=url,
        )

        metadata = []
        for a in soup.select('.film-info a[href*="genre"]'):
            metadata.append(Metadata('subject', a.text.strip()))

        chapters = []
        for i, div in enumerate(soup.select('#list-chapters > .book')):
            volume = (i, div.select_one('.title a').text.strip())

            for a in div.select('.list-chapters > li a'):
                chapter = Chapter(
                    index=len(chapters),
                    title=a.text.strip(),
                    volume=volume,
                    url=self.base_urls[0] + a['href'],
                )

                chapters.append(chapter)

        return novel, chapters, metadata

    def chapter(self, chapter: Chapter):
        soup = self.soup(chapter.url)

        contents = soup.select_one('#chapter-body')
        self.clean_contents(contents)

        for element in contents.select('.language'):
            element.extract()

        chapter.paragraphs = str(contents)
