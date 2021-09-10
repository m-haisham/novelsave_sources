import datetime

from .source import Source
from ...models import Novel, Chapter, Metadata


class NovelOnlineFull(Source):
    base_urls = ('https://novelonlinefull.com',)
    last_updated = datetime.date(2021, 9, 7)

    blacklist_patterns = [
        r'^[\W\D]*(volume|chapter)[\W\D]+\d+[\W\D]*$',
        r'^(\s| )+$',  # non-breaking whitespace
    ]

    def novel(self, url: str) -> Novel:
        soup = self.get_soup(url)

        synopsis_parent = soup.select_one('#noidungm')
        [e.extract() for e in synopsis_parent.select('h2, [style*="color"]')]

        novel = Novel(
            title=soup.select_one('.truyen_info_wrapper h1').text,
            thumbnail_url=soup.select_one('.info_image img')['src'],
            synopsis=self.find_paragraphs(synopsis_parent),
            url=url,
        )

        alternative = soup.select_one('.truyen_info_wrapper .truyen_info_right > li:first-child > span')
        if alternative:
            novel.metadata.append(Metadata('author', alternative.text.strip('Alternative :').strip(), others={'role': 'alternative'}))

        for li in soup.select('.truyen_info_wrapper .truyen_info_right > li'):
            span = li.select_one('span')
            if not span:
                continue

            label = span.text.strip()
            if label == 'Author(s):':
                novel.author = ', '.join([a.text.strip() for a in li.select('a')])
            elif label == 'GENRES:':
                for a in li.select('a'):
                    novel.metadata.append(Metadata('subject', a.text.strip()))

        volume = novel.get_default_volume()
        for i, a in enumerate(reversed(soup.select('.chapter-list > .row a'))):
            chapter = Chapter(
                index=i,
                title=a.text.strip(),
                url=a['href'],
            )

            volume.chapters.append(chapter)

        return novel

    def chapter(self, chapter: Chapter):
        soup = self.get_soup(chapter.url)

        content = soup.select_one('#vung_doc')
        self.clean_contents(content)

        chapter.paragraphs = str(content)
