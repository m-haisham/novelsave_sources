import datetime
import re

from .source import Source
from ...models import Chapter, Novel, Metadata


class NovelHall(Source):
    base_urls = ('https://www.novelhall.com',)
    last_updated = datetime.date(2021, 9, 7)

    def novel(self, url: str) -> Novel:
        soup = self.get_soup(url)

        synopsis_element = soup.select_one('.js-close-wrap')
        synopsis_element.select_one('span').extract()

        novel = Novel(
            title=soup.select_one('.book-info h1').text.strip(),
            thumbnail_url=soup.select_one('.book-img img')['src'],
            synopsis=[t.strip() for t in synopsis_element.text.splitlines() if t.strip()],
            url=url,
        )

        for span in soup.select('.booktag span.blue'):
            for text in span.find_all(text=True, recursive=False):
                _text = str(text).strip()
                if _text.startswith('Author：'):
                    novel.author = _text.lstrip('Author：')
                    break

        for a in soup.select('.booktag a[href*="genre"]'):
            novel.metadata.append(Metadata('subject', a.text.strip()))

        volume = novel.get_default_volume()
        for i, a in enumerate(soup.select('#morelist > ul li a')):
            chapter = Chapter(
                index=i,
                title=a.text.strip(),
                url=self.base_urls[0] + a['href'],
            )

            volume.chapters.append(chapter)

        return novel

    def chapter(self, chapter: Chapter):
        soup = self.get_soup(chapter.url)

        content = soup.select_one('.entry-content')
        self.clean_contents(content)

        content.unwrap()
        content = '<p>' + re.sub(r'<br ?/?>', '</p><p>', str(content).strip()) + '</p>'

        chapter.title = soup.select_one('.single-header h1').text.strip()
        chapter.paragraphs = content
