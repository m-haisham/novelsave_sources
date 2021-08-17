import re
from typing import Tuple, List

from .source import Source
from ...models import Novel, Chapter, Metadata


class WuxiaCo(Source):
    name = 'WuxiaWorld.co'
    base_urls = ('https://www.wuxiaworld.co',)

    def novel(self, url: str) -> Tuple[Novel, List[Chapter], List[Metadata]]:
        soup = self.soup(url)

        novel = Novel(
            title=soup.find('div', {'class': 'book-name'}).text,
            author=soup.find('div', {'class': 'author'}).find('span', {'class': 'name'}).text,
            synopsis=soup.find('div', {'class': 'synopsis'}).find('p').text,
            thumbnail_url=soup.find('div', {'class': 'book-img'}).find('img')['src'],
            url=url
        )

        chapters = []
        for i, item in enumerate(soup.find_all('a', {'class': 'chapter-item'})):
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

            chapters.append(chapter)

        return novel, chapters, []

    def chapter(self, chapter: Chapter):
        soup = self.soup(chapter.url)

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
