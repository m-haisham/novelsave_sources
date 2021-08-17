import re
from typing import List, Tuple

from .source import Source
from ...models import Chapter, Novel, Metadata


class NovelHall(Source):
    base_urls = ('https://www.novelhall.com',)

    def novel(self, url: str) -> Tuple[Novel, List[Chapter], List[Metadata]]:
        soup = self.soup(url)
        metadata = []

        synopsis_element = soup.select_one('.js-close-wrap')
        synopsis_element.select_one('span').extract()

        novel = Novel(
            title=soup.select_one('.book-info h1').text.strip(),
            thumbnail_url=soup.select_one('.img-thumbnail_url')['src'],
            synopsis=synopsis_element.text.strip(),
            url=url,
        )

        for span in soup.select('.booktag span.blue'):
            for text in span.find_all(text=True, recursive=False):
                _text = str(text).strip()
                if _text.startswith('Author：'):
                    novel.author = _text.lstrip('Author：')
                    break

        for a in soup.select('.booktag a[href*="genre"]'):
            metadata.append(Metadata('subject', a.text.strip()))

        chapters = []
        for i, a in enumerate(soup.select('#morelist > ul li a')):
            chapter = Chapter(
                index=i,
                title=a.text.strip(),
                url=self.base_urls[0] + a['href'],
            )

            chapters.append(chapter)

        return novel, chapters, metadata

    def chapter(self, chapter: Chapter):
        soup = self.soup(chapter.url)

        content = soup.select_one('.entry-content')
        self.clean_contents(content)

        content = '<p>' + re.sub(r'<br ?/?>', '</p><p>', str(content).strip('<div></div>').strip()) + '</p>'

        chapter.title = soup.select_one('.single-header h1').text.strip()
        chapter.paragraphs = content
