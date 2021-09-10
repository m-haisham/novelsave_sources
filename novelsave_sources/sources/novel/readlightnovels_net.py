import datetime

from bs4 import BeautifulSoup

from .source import Source
from ...models import Novel, Volume, Chapter, Metadata


class ReadLightNovelsNet(Source):
    name = 'Read Light Novels'
    base_urls = ('https://readlightnovels.net',)
    last_updated = datetime.date(2021, 9, 6)

    def novel(self, url: str) -> Novel:
        soup = self.get_soup(url)

        authors = [a.text.strip() for a in soup.select('.info a[href*="novel-author"]')]
        if len(authors) == 2:
            author = f'{authors[0]} ({authors[1]})'
        else:
            author = ', '.join(authors)

        title = soup.select_one('.title').text.strip()
        if title.endswith(' Novel'):
            title = title[:-len(' Novel')]

        novel = Novel(
            title=title,
            author=author,
            synopsis=[p.text.strip() for p in soup.select('.desc-text > p')],
            thumbnail_url=soup.select_one('.info-holder img')['src'],
            url=url
        )

        for a in soup.select('a[rel*="tag"]'):
            novel.metadata.append(Metadata('subject', a.text.strip()))

        pages = soup.select('#pagination > ul > li:not(.dropup) a:last-child')
        pages_count = int(pages[-1]['title']) if pages else 0
        novel_id = soup.select_one('#id_post')['value']
        volume = novel.get_default_volume()

        for page_index in range(pages_count + 1):
            self.chapter_page(volume, novel_id, page_index + 1)

        return novel

    def chapter_page(self, volume: Volume, novel_id, page):
        response = self.session.post(
            'https://readlightnovels.net/wp-admin/admin-ajax.php',
            data={
                'action': 'tw_ajax',
                'type': 'pagination',
                'id': novel_id,
                'page': page,
            },
        )

        soup = BeautifulSoup(response.json()['list_chap'], 'lxml')
        for a in soup.select('ul.list-chapter li a'):
            chapter = Chapter(
                index=len(volume.chapters),
                title=a.text.strip(),
                url=a['href'],
            )

            volume.chapters.append(chapter)

    def chapter(self, chapter: Chapter):
        soup = self.get_soup(chapter.url)

        content = soup.select_one('.chapter-content')
        self.clean_contents(content)
        for br in content.select('br'):
            br.extract()

        chapter.paragraphs = str(content)
