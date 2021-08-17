import re
from typing import Tuple, List

from .source import Source
from ...models import Novel, Chapter, Metadata


class Ktlchamber(Source):
    base_urls = ('https://ktlchamber.wordpress.com',)

    chapter_regex = re.compile(r'Chapter[  ](\d+)\.[  ]?(.*)', flags=re.IGNORECASE)

    def novel(self, url: str) -> Tuple[Novel, List[Chapter], List[Metadata]]:
        soup = self.soup(url)

        entry_content = soup.find('div', {'class': 'entry-content'})

        author = ''
        for p in entry_content.find_all('p'):
            text = p.text
            if text.startswith('Author: '):
                author = text.split(': ', maxsplit=1)[1]

        novel = Novel(
            title=soup.find('h1', {'class': 'entry-title'}).text,
            thumbnail_url=entry_content.find('img')['src'],
            author=author,
            url=url,
        )

        offset = 0
        chapters = []
        prefix = f"{url}{'' if url[-1] == '/' else '/'}"
        for a in entry_content.find_all('a'):
            text = a.text
            if text.startswith('Chapter'):
                result = self.chapter_regex.search(text)

                chapter = Chapter(
                    index=offset,
                    no=int(result.group(1)),
                    title=result.group(2),
                    url=f"{prefix}{a['href']}"
                )

                chapters.append(chapter)
                offset += 1

        for i, li in enumerate(entry_content.find('ul', recursive=False).children):
            a = li.find('a')

            result = self.chapter_regex.search(a.text)
            chapter = Chapter(
                index=offset + i,
                no=int(result.group(1)),
                title=result.group(2),
                url=a['href']
            )

            chapters.append(chapter)

        return novel, chapters, []

    def chapter(self, chapter: Chapter):
        soup = self.soup(chapter.url)

        entry_content = soup.find('div', {'class': 'entry-content'})
        p_elements = entry_content.find_all('p')

        paragraphs = []
        for element in p_elements[1:-1]:
            for text in element.find_all(text=True):
                paragraphs.append(text.strip())

        result = self.chapter_regex.search(soup.find('h1', {'class': 'entry-title'}).text)

        chapter.title = result.group(2)
        chapter.paragraphs = paragraphs
