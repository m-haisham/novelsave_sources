import re
from typing import Tuple, List

from .source import Source
from ...models import Novel, Chapter, Metadata


class LightNovelWorld(Source):
    base_urls = ('https://www.lightnovelworld.com',)

    chapter_title_regex = re.compile(r'chapter (\d+\.?\d*):? ?(.+)?', flags=re.IGNORECASE)

    def novel(self, url: str) -> Tuple[Novel, List[Chapter], List[Metadata]]:
        soup = self.soup(url)

        novel = Novel(
            title=soup.find('h1', {'class': 'novel-title'}).text,
            author=soup.find('div', {'class': 'author'}).find('a').text.strip(),
            thumbnail_url=soup.find('figure', {'class': 'cover'}).find('img')['src'],
            url=url,
        )

        chapters = []
        for i, li in enumerate(soup.find('ul', {'class': 'chapter-list'}).children):
            a = li.find('a')

            chapter = Chapter(
                index=i,
                url=LightNovelWorld.base_urls[0] + a['href'],
            )

            chapters.append(chapter)

        return novel, chapters, []

    def chapter(self, chapter: Chapter):
        soup = self.soup(chapter.url)

        title_element = soup.find('div', {'class': 'titles'}).find('h2')
        result = self.chapter_title_regex.search(title_element.text)
        if len(result.groups()) > 1:
            chapter.title = result.group(2)
        else:
            chapter.title = title_element.text.strip()

        chapter.paragraphs = []
        chapter_content = soup.find('div', {'class': 'chapter-content'})
        for text in chapter_content.find_all(text=True):
            chapter.paragraphs.append(text.strip())

        return chapter
