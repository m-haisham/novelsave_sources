import datetime

from .source import Source
from ...models import Chapter, Novel, Metadata


class WuxiaCom(Source):
    name = 'WuxiaWorld.com'
    base_urls = ('https://www.wuxiaworld.com',)
    last_updated = datetime.date(2021, 9, 4)

    blacklist_patterns = [
        r'^<span>(...|\u2026)</span>$',
        r'^translat(ed by|or)',
        r'(volume|chapter) .?\d+',
    ]

    def novel(self, url: str) -> Novel:
        soup = self.get_soup(url)

        novel = Novel(
            title=soup.select_one('.section-content h2').text,
            synopsis=[p.text.strip() for p in soup.select('.fr-view:not(.pt-10) p')],
            thumbnail_url=soup.select_one('img.media-object').get('src'),
            url=url,
        )

        author_elements = soup.select('.novel-body :is(dt, dd)')
        for i, element in enumerate(author_elements):
            if element.name != 'dt':
                continue

            head = element.text.strip()
            if head == 'Translator:':
                novel.metadata.append(Metadata('contributor', author_elements[i + 1].text.strip()))
            elif head == 'Author:':
                novel.author = author_elements[i + 1].text.strip()

        for a in soup.select('.genres a'):
            novel.metadata.append(Metadata('subject', a.text.strip()))

        volume = novel.get_default_volume()
        for panel in soup.select('#accordion .panel-default'):
            for a in panel.select('ul.list-chapters li.chapter-item a'):
                chapter = Chapter(
                    index=len(volume.chapters),
                    title=a.text.strip(),
                    url=self.base_urls[0] + a['href'],
                )

                volume.chapters.append(chapter)

        return novel

    def chapter(self, chapter: Chapter):
        soup = self.get_soup(chapter.url)

        contents = soup.select_one('#chapterContent')
        if not contents:
            contents = soup.select_one('#chapter-content')
        if not contents:
            contents = soup.select_one('.panel-default .fr-view')
        if not contents:
            raise ValueError(f'Unable to read chapter content from {chapter}')

        for nav in (contents.select('.chapter-nav') or []):
            nav.extract()

        self.clean_contents(contents)

        chapter.title = soup.select_one('#chapter-outer  h4').text.strip()
        chapter.paragraphs = str(contents)
