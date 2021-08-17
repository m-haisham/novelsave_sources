from typing import Tuple, List

from .source import Source
from ...models import Novel, Chapter, Metadata


class NovelOnlineFull(Source):
    base_urls = ('https://novelonlinefull.com',)

    blacklist_patterns = [
        r'^[\W\D]*(volume|chapter)[\W\D]+\d+[\W\D]*$',
        r'^(\s| )+$',  # non-breaking whitespace
    ]

    def novel(self, url: str) -> Tuple[Novel, List[Chapter], List[Metadata]]:
        soup = self.soup(url)
        metadata = []

        synopsis_parent = soup.select_one('#noidungm')
        synopsis_parent.select_one('h2').extract()
        synopsis_elements = synopsis_parent.find_all(text=True, recursive=False)
        synopsis = '\n'.join([str(element).strip() for element in synopsis_elements]).strip()

        novel = Novel(
            title=soup.select_one('.truyen_info_wrapper h1').text,
            thumbnail_url=soup.select_one('.info_image img')['src'],
            synopsis=synopsis,
            url=url,
        )

        alternative = soup.select_one('.truyen_info_wrapper .truyen_info_right > li:first-child > span')
        if alternative:
            metadata.append(Metadata('author', alternative.text.strip('Alternative :').strip(), others={'role': 'alternative'}))

        for li in soup.select('.truyen_info_wrapper .truyen_info_right > li'):
            span = li.select_one('span')
            if not span:
                continue

            label = span.text.strip()
            if label == 'Author(s):':
                novel.author = ', '.join([a.text.strip() for a in li.select('a')])
            elif label == 'GENRES:':
                for a in li.select('a'):
                    metadata.append(Metadata('subject', a.text.strip()))

        chapters = []
        for i, a in enumerate(reversed(soup.select('.chapter-list > .row a'))):
            chapter = Chapter(
                index=i,
                title=a.text.strip(),
                url=a['href'],
            )

            chapters.append(chapter)

        return novel, chapters, metadata

    def chapter(self, chapter: Chapter):
        soup = self.soup(chapter.url)

        content = soup.select_one('#vung_doc')
        self.clean_contents(content)

        chapter.paragraphs = str(content)
