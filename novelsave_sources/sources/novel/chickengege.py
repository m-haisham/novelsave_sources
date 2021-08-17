from typing import Tuple, List

from .source import Source
from ...models import Novel, Chapter, Metadata


class ChickEngege(Source):
    base_urls = ('https://www.chickengege.org',)

    def novel(self, url: str) -> Tuple[Novel, List[Chapter], List[Metadata]]:
        soup = self.soup(url)
        metadata = []

        thumbnail_element = soup.select_one('.novelist-cover-image')

        novel = Novel(
            title=soup.select_one('.entry-title').text.strip(),
            thumbnail_url=thumbnail_element and thumbnail_element['src'],
            url=url,
        )

        for element in soup.select('.entry-content > div strong'):
            text = element.text.strip()
            if text == 'Original Title:':
                metadata.append(Metadata('title', element.findNext('span').text.strip(), others={'type': 'original'}))
            elif text == 'Synopsis:':
                lines = []
                for text in element.parent.find_all(text=True):
                    if text == 'Synopsis:':
                        continue

                    text = text.strip()
                    if text:
                        lines.append(text)

                while True:
                    element = element.findNext()
                    if element.name == 'hr':
                        break

                    lines.append(element.text.strip())

                novel.synopsis = '\n'.join(lines)

            elif text == 'Translator(s):':
                ul = element.findNext('ul')
                for a in ul.select('li > a'):
                    metadata.append(Metadata('contributor', a.text.strip(), others={'role': 'translator'}))
            elif text == 'Editor(s):':
                ul = element.findNext('ul')
                for a in ul.select('li > a'):
                    metadata.append(Metadata('contributor', a.text.strip(), others={'role': 'editor'}))

        for a in soup.select('a[rel="tag"]'):
            metadata.append(Metadata('subject', a.text.strip()))

        chapters = []
        for a in soup.select('#novelList > li > a'):
            chapter = Chapter(
                index=len(chapters),
                title=a.text.strip(),
                url=a['href'],
            )

            chapters.append(chapter)

        return novel, chapters, metadata

    def chapter(self, chapter: Chapter):
        soup = self.soup(chapter.url)

        content = soup.select_one('.entry-wrap .entry-content')
        self.clean_contents(content)

        chapter.title = soup.select_one('.entry-title').text.strip()
        chapter.paragraphs = str(content)
