import datetime
from typing import List

from .source import Source
from ...models import Novel, Chapter, Metadata


class RainOfSnow(Source):
    name = 'Rain Of Snow Translations'
    base_urls = ('https://rainofsnow.com/',)
    last_updated = datetime.date(2021, 9, 4)

    def novel(self, url: str) -> Novel:
        soup = self.get_soup(url)

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
                novel.metadata.append(Metadata('contributor', value, others={'role': 'translator'}))

            elif key.lower() == 'editor':
                novel.metadata.append(Metadata('contributor', value, others={'role': 'editor'}))

            elif key.lower() == 'genre(s)':
                for word in value.split(','):
                    if not word.strip():
                        continue
                    novel.metadata.append(Metadata('subject', word.strip()))

            elif key.lower() == 'type':
                novel.metadata.append(Metadata('type', value))

        for tag in soup.select('.vbtcolor1 > li a[href*="tag"]'):
            novel.metadata.append(Metadata('tag', tag.strip()))

        volume = novel.get_default_volume()
        for a in soup.select('#chapter .chapter a'):
            chapter = Chapter(
                index=len(volume.chapters),
                title=a.text.strip(),
                url=a['href'],
            )

            volume.chapters.append(chapter)

        return novel

    @staticmethod
    def synopsis(soup) -> List[str]:
        paragraphs = []
        for element in soup.select('#synop > p'):
            if not element.text.strip():
                continue

            paragraphs.append(element.text)

        return paragraphs

    def chapter(self, chapter: Chapter):
        soup = self.get_soup(chapter.url)

        content = soup.select_one('.bb-item[style*="block"] .content .scroller .zoomdesc-cont')
        content = self.clean_contents(content)

        chapter.paragraphs = str(content)
