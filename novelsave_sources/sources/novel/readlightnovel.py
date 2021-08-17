import re
import unicodedata
from typing import Tuple, List

from .source import Source
from ...models import Novel, Chapter, Metadata


class ReadLightNovel(Source):
    name = 'Read Light Novel'
    base_urls = ('https://www.readlightnovel.org',)

    def novel(self, url: str) -> Tuple[Novel, List[Chapter], List[Metadata]]:
        soup = self.soup(url)

        # parse author
        author = None
        for element in soup.find('div', {'class': 'novel-left'}).find_all('div', {'class': 'novel-detail-item'}):
            if element.find('div', {'class': 'novel-detail-header'}).text.strip() == 'Author(s)':
                author = element.find('div', {'class': 'novel-detail-body'}).find('li').text.strip()
                break

        novel = Novel(
            title=soup.find('div', {'class': 'block-title'}).text.strip(),
            author=author,
            synopsis=soup.select_one('.novel-right .novel-detail-item .novel-detail-body').text.strip(),
            thumbnail_url=soup.find('div', {'class': 'novel-cover'}).find('img')['src'],
            url=url
        )

        chapters = []
        for i, element in enumerate(
                soup.find('div', {'class': 'tab-content'}).find_all('ul', {'class': 'chapter-chs'})
        ):
            children = list(element.find_all('a'))
            offset = len(children) * i
            for j, link in enumerate(children):

                chapter = Chapter(
                    index=offset + j,
                    title=link.text.strip(),
                    url=link['href']
                )

                chapters.append(chapter)

        return novel, chapters, []

    def chapter(self, chapter: Chapter):
        soup = self.soup(chapter.url)

        content = soup.find('div', {'class': 'chapter-content3'}).find('div', {'class': 'desc'})

        title_element = content.find('h3')

        title = None
        if title_element is not None:
            # title can have some unicode characters in them
            title = unicodedata.normalize("NFKD", title_element.text)

        # paragraphs
        paragraphs = []

        if content.find('p') is None:
            # no <p> elements
            for text in content.find_all(text=True, recursive=False):
                paragraphs.append(text)
        else:
            para_elements = content.find_all('p', recursive=False)
            for element in para_elements:
                text = element.text.strip()
                paragraphs.append(text)

        # fixing the formatting issue
        for i in range(len(paragraphs)):
            paragraphs[i] = re.sub(r' \. ?', '. ', paragraphs[i]).strip()

        chapter.title = title
        chapter.paragraphs = paragraphs
