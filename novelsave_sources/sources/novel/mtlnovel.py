import datetime

from .source import Source
from ...models import Chapter, Novel, Metadata


class MtlNovel(Source):
    name = 'MTL Novel'
    base_urls = (
        'https://www.mtlnovel.com',
        'http://www.mtlnovel.com',
    )
    last_updated = datetime.date(2021, 9, 7)

    def novel(self, url: str) -> Novel:
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
            synopsis=[p.text.strip() for p in soup.select('.desc > p:not(.descr)')],
            thumbnail_url=soup.select_one('.main-tmb')['src'],
            url=url,
        )

        # metadata
        alt_title = soup.select_one('#alt')
        if alt_title:
            novel.metadata.append(Metadata('title', alt_title.text.strip(), others={'role': 'alt'}))

        for genre in soup.select('#genre a'):
            novel.metadata.append(Metadata('subject', genre.text.strip()))

        for tag in soup.select('#tags a:not(.edit-history-button)'):
            novel.metadata.append(Metadata('tag', tag.text.strip()))

        novel.metadata.append(Metadata('status', soup.select_one('#status').text.strip()))

        # chapter list
        chapter_list_url = http_url.rstrip('/') + '/chapter-list/'
        soup = self.get_soup(chapter_list_url)

        volume = novel.get_default_volume()
        for i, a in enumerate(reversed(soup.select('.ch-list .ch-link'))):

            chapter = Chapter(
                index=i,
                title=a.text.strip(),
                url=a['href'],
            )

            volume.chapters.append(chapter)

        return novel

    def chapter(self, chapter: Chapter):
        soup = self.get_soup(chapter.url)

        paragraphs = soup.select_one('.par')
        self.clean_contents(paragraphs)

        # remove ad frames
        for frame in paragraphs.select('amp-iframe, .ads'):
            frame.decompose()

        chapter.title = soup.select_one('.current-crumb').text.strip()
        chapter.paragraphs = str(paragraphs)
