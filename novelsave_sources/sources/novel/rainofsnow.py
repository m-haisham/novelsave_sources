from typing import Tuple, List

from .source import Source
from ...models import Novel, Chapter, Metadata


class RainOfSnow(Source):
    name = 'Rain Of Snow Translations'

    base_urls = ('https://rainofsnow.com/',)

    def novel(self, url: str) -> Tuple[Novel, List[Chapter], List[Metadata]]:
        soup = self.soup(url)
        metadata = []

        novel = Novel(
            title=soup.select_one('.text h2').text.strip(),
            synopsis=self.synopsis(soup),
            thumbnail_url=soup.select_one('.imagboca1 img')['data-src'],
            url=url,
        )

        for li in soup.select('.vbtcolor1 > li'):
            key, value = li.select_one('.vt1').text.strip(), li.select_one('.vt2').text.strip()
            if key.lower() == 'author':
                novel.author = value
            elif key.lower() == 'translator':
                metadata.append(Metadata('author', value, others={'role': 'translator'}))
            elif key.lower() == 'editor':
                metadata.append(Metadata('author', value, others={'role': 'editor'}))
            elif key.lower() == 'genre(s)':
                for word in value.split(','):
                    metadata.append(Metadata('subject', word.strip()))
            elif key.lower() == 'type':
                metadata.append(Metadata('type', value))

        # tags selector: .vbtcolor1 > li a[href*="tag"]

        chapters = []
        for a in soup.select('#chapter .chapter a'):
            chapter = Chapter(
                index=len(chapters),
                title=a.text.strip(),
                url=a['href'],
            )

            chapters.append(chapter)

        return novel, chapters, metadata

    def synopsis(self, soup) -> str:
        paragraphs = []
        for element in soup.select('#synop > p'):
            if not element.text.strip():
                continue

            paragraphs.append(element.text)

        return '\n'.join(paragraphs)

    def chapter(self, chapter: Chapter):
        soup = self.soup(chapter.url)

        content = soup.select_one('.bb-item[style*="block"] .content .scroller .zoomdesc-cont')
        content = self.clean_contents(content)

        chapter.paragraphs = str(content)
