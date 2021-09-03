import datetime
from urllib.parse import parse_qs, urlparse

from bs4 import BeautifulSoup

from .source import Source
from ...models import Chapter, Volume, Novel, Metadata


class WuxiaSite(Source):
    name = 'WuxiaWorld.site'
    base_urls = ('https://wuxiaworld.site',)
    last_updated = datetime.date(2021, 9, 3)

    def novel(self, url: str) -> Novel:
        soup = self.get_soup(url)

        title = ' '.join([
            str(x)
            for x in soup.select_one('.post-title').select_one('h1, h2, h3').contents
            if not x.name
        ]).strip()

        author = soup.select('.author-content a')
        if len(author) == 2:
            author = author[0].text + ' (' + author[1].text + ')'
        else:
            author = author[0].text

        novel = Novel(
            title=title,
            author=author,
            thumbnail_url=soup.select_one('.summary_image a img')['srcset'].split(' ', maxsplit=1)[0],
            synopsis=[str(p).strip() for p in soup.select_one('.summary__content > p:nth-child(2)').find_all(text=True, recursive=False)],
            url=url,
        )

        for a in soup.select('.artist-content > a'):
            novel.metadata.append(Metadata('contributor', a.text.strip(), others={'role': 'illustrator'}))

        for a in soup.select('a[href*="genre"][rel="tag"]'):
            novel.metadata.append(Metadata('subject', a.text.strip()))

        shortlink = soup.select_one('link[rel="shortlink"]')['href']
        novel_id = int(parse_qs(urlparse(shortlink).query).get('p')[0])
        response = self.request(
            'POST',
            'https://wuxiaworld.site/wp-admin/admin-ajax.php',
            data={
                'action': 'manga_get_chapters',
                'manga': novel_id,
            }
        )

        soup = BeautifulSoup(response.content, 'lxml')

        volume = Volume.default()
        novel.volumes.append(volume)
        for a in reversed(soup.select('li.wp-manga-chapter a')):
            index = len(volume.chapters)
            chapter = Chapter(
                index=index,
                title=a.text.strip() or f'Chapter {index}',
                url=a['href'],
            )

            volume.chapters.append(chapter)

        return novel

    def chapter(self, chapter: Chapter):
        soup = self.get_soup(chapter.url)

        contents = soup.select('.text-left p, .cha-words p')
        body = [str(p) for p in contents if p.text.strip()]

        chapter.paragraphs = ''.join(body)
