import datetime
from typing import List, Tuple

from .source import Source
from ...models import Chapter, Novel, Metadata


class MtlNovel(Source):
    name = 'MTL Novel'
    base_urls = ('https://www.mtlnovel.com',)
    last_updated = datetime.date(2021, 8, 30)

    def novel(self, url: str) -> Tuple[Novel, List[Chapter], List[Metadata]]:
        http_url = url.replace('https://', 'http://')
        soup = self.get_soup(http_url)

        author = ''
        info_element = soup.select_one('.info > tbody')
        for element in info_element.select('tr'):
            text = element.text
            if text.startswith('Author:'):
                author = text[7:]
                break
        
        novel = Novel(
            title=soup.select_one('.entry-title').text.strip(),
            author=author,
            synopsis='\n'.join(p.text.strip() for p in soup.select('.desc > p:not(.descr)')),
            thumbnail_url=soup.select_one('.main-tmb')['src'],
            url=url,
        )

        # metadata
        metadata = []
        alt_title = soup.select_one('#alt')
        if alt_title:
            metadata.append(Metadata.custom('title', alt_title.text.strip(), others={'role': 'alt'}))

        for genre in soup.select('#genre a'):
            metadata.append(Metadata('subject', genre.text.strip()))

        for tag in soup.select('#tags a:not(.edit-history-button)'):
            metadata.append(Metadata.custom('tag', tag.text.strip()))

        metadata.append(Metadata.custom('status', soup.select_one('#status').text.strip()))

        # chapter list
        chapter_list_url = http_url.rstrip('/') + '/chapter-list/'
        soup = self.get_soup(chapter_list_url)

        chapters = []
        for i, a in enumerate(reversed(soup.select('.ch-list .ch-link'))):

            chapter = Chapter(
                index=i,
                title=a.text.strip(),
                url=a['href'],
            )

            chapters.append(chapter)

        return novel, chapters, metadata

    def chapter(self, chapter: Chapter):
        soup = self.get_soup(chapter.url)

        paragraphs = soup.select_one('.par')
        self.clean_contents(paragraphs)

        # remove ad frames
        for frame in paragraphs.select('amp-iframe'):
            frame.decompose()

        chapter.title = soup.select_one('.current-crumb').text.strip()
        chapter.paragraphs = str(paragraphs)
