import datetime
import re
from typing import List

from .source import Source
from ...models import Novel, Volume, Chapter, Metadata


class WuxiaCo(Source):
    name = 'WuxiaWorld.co'
    base_urls = ('https://www.wuxiaworld.co',)
    last_updated = datetime.date(2021, 9, 4)

    @classmethod
    def of(cls, url: str) -> bool:
        return url.startswith(cls.base_urls[0] + '/')

    def novel(self, url: str) -> Novel:
        soup = self.get_soup(url)

        novel = Novel(
            title=soup.select_one('.book-name').text.strip(),
            author=soup.select_one('.author span.name').text.strip(),
            synopsis=[p.text.strip() for p in soup.select('div.synopsis p')],
            thumbnail_url=soup.select_one('.book-img img')['src'],
            url=url
        )

        catalog = soup.select_one('.book-catalog .txt')
        if catalog:
            novel.metadata.append(Metadata('subject', catalog.text.strip()))

        volume = Volume.default()
        novel.volumes.append(volume)
        for i, item in enumerate(soup.select('a.chapter-item')):
            # wuxiaco uses inline styling(color) to show that chapter isn't ready yet
            # no need to download chapters without actual content
            if 'style' in item.attrs.keys():
                continue

            title = item.find('p').text

            chapter = Chapter(
                index=i,
                title=title,
                url=self.base_urls[0] + item['href'],
            )

            volume.chapters.append(chapter)

        return novel

    def chapter(self, chapter: Chapter):
        soup = self.get_soup(chapter.url)

        title = soup.find('h1', {'class': 'chapter-title'}).text

        # remove google ads
        for element in soup.find_all('ins', {'class': 'adsbygoogle'}):
            element.decompose()

        content = [
            text.strip()
            for text in soup.find('div', {'class': 'chapter-entity'}).find_all(text=True, recursive=False)
        ]

        # removes random junk inside paragraphs
        # including new-line, tab
        #
        content = self._clean_content(content)

        chapter.title = title
        chapter.paragraphs = '<p>' + '</p><p>'.join(content) + '</p>'

    def _clean_content(self, content) -> List[str]:
        paragraphs = []

        # check is paragraph has line breaks or tabs inside
        # if split to separate paragraphs
        for i, para in enumerate(content):
            para = re.sub(r'[\n\t\r]', ' ', para)

            parts = [part.strip() for part in para.split('  ') if part]

            # filter out junk lines
            p = ' '.join((
                part
                for part in parts
                if part not in ['Please go to', 'to read the latest chapters for free']
            ))

            paragraphs.append(p)

        return paragraphs
