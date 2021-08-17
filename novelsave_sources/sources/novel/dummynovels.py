from typing import Tuple, List

from .source import Source
from ...models import Novel, Chapter, Metadata


class DummyNovels(Source):
    name = 'Dummy novels'
    base_urls = ('https://dummynovels.com',)

    def novel(self, url: str) -> Tuple[Novel, List[Chapter], List[Metadata]]:
        soup = self.soup(url)
        metadata = []

        synopsis_content = soup.select('.novel-synopsis-content > p')
        synopsis = '\n'.join([element.text.strip() for element in synopsis_content])

        novel = Novel(
            title=soup.select_one('h1.elementor-heading-title').text.strip(),
            thumbnail_url=soup.select_one('.elementor-image img')['src'],
            synopsis=synopsis,
            url=url,
        )

        for element in soup.select('.elementor-widget-text-editor'):
            text = element.text.strip()
            if text.startswith('Author: '):
                novel.author = text.lstrip('Author: ')
            elif text.startswith('Translator: '):
                metadata.append(Metadata('contributor', text.strip('Translator: '), others={'role': 'translator'}))
            elif text.startswith('Editors: '):
                metadata.append(Metadata('contributor', text.strip('Editors: '), others={'role': 'editor'}))

        for element in soup.select('.novel-term > a'):
            metadata.append(Metadata('subject', element.text.strip()))

        chapters = []
        for element in soup.select('.elementor-tab-content a[href*="novel"]:not(.elementor-accordion-title)'):

            # this removes the text '(NEW)'
            highlight = element.select_one('.new-highlight')
            if highlight:
                highlight.extract()

            chapter = Chapter(
                index=len(chapters),
                title=element.text.strip(),
                url=element['href'],
            )

            chapters.append(chapter)

        return novel, chapters, metadata

    def chapter(self, chapter: Chapter):
        soup = self.soup(chapter.url)

        content = soup.select_one('.elementor-widget-theme-post-content > div')

        # removes ads
        for element in content.select('.code-block'):
            element.extract()

        self.clean_contents(content)

        chapter.title = soup.select_one('.chapter-heading:not(.novel-title-for-chapters)').text.strip()
        chapter.paragraphs = str(content)
