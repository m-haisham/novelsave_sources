import datetime
import re

from .source import Source
from ...models import Novel, Chapter, Metadata


class LightNovelWorld(Source):
    base_urls = ('https://www.lightnovelworld.com',)
    last_updated = datetime.date(2021, 9, 7)

    chapter_title_regex = re.compile(r'chapter (\d+\.?\d*):? ?(.+)?', flags=re.IGNORECASE)

    def novel(self, url: str) -> Novel:
        soup = self.get_soup(url)

        novel = Novel(
            title=soup.select_one('.novel-title').text.strip(),
            author=soup.select_one('.author a').text.strip(),
            thumbnail_url=soup.select_one('figure.cover img')['src'],
            synopsis=self.find_paragraphs(soup.select_one('.summary .content'), recursive=True),
            url=url,
        )

        for a in soup.select('.categories a'):
            novel.metadata.append(Metadata('subject', a.text.strip()))

        for a in soup.select('.tags a'):
            novel.metadata.append(Metadata('tag', a.text.strip()))

        novel.metadata.append(Metadata('status', soup.select_one('.completed, .ongoing').text.strip()))

        self.parse_toc(novel)

        return novel

    def parse_toc(self, novel):
        volume = novel.get_default_volume()

        # first page
        url = novel.url.rstrip("/") + '/chapters'
        soup = self.get_soup(url)

        last_page = soup.select_one('.PagedList-skipToLast a') or soup.select('.pagination li:not([class]) a')[-1]
        page_count = int(last_page['href'].rsplit('-', maxsplit=1)[-1])

        # get the rest of the pages
        for page in range(1, page_count + 1):
            url = f'{novel.url.rstrip("/")}/chapters/page-{page}'
            soup = self.get_soup(url)

            self.parse_toc_page(soup, volume)

    def parse_toc_page(self, soup, volume):
        for li in soup.select('.chapter-list li[data-chapterno]'):
            a = li.select_one('a')
            chapter = Chapter(
                index=len(volume.chapters),
                title=a.select_one('strong').text.strip(),
                url=self.to_absolute_url(a['href']),
            )

            volume.chapters.append(chapter)

    def chapter(self, chapter: Chapter):
        soup = self.get_soup(chapter.url)

        title_element = soup.find('div', {'class': 'titles'}).find('h2')
        result = self.chapter_title_regex.search(title_element.text)
        if len(result.groups()) > 1:
            chapter.title = result.group(2)
        else:
            chapter.title = title_element.text.strip()

        content = soup.select('.chapter-content > p:not([class])')
        chapter.paragraphs = ''.join(str(p) for p in content)
