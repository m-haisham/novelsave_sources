import datetime
from urllib.parse import urlparse, parse_qs

from bs4 import BeautifulSoup

from .source import Source
from ...models import Chapter, Novel, Metadata


class NovelSite(Source):
    base_urls = ('https://novelsite.net',)
    last_updated = datetime.date(2021, 9, 6)

    def __init__(self):
        super(NovelSite, self).__init__()
        self.bad_tags.extend([
            'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
        ])

    def novel(self, url: str) -> Novel:
        soup = self.get_soup(url)

        authors = [a.text.strip() for a in soup.select('.author-content > a')]
        if len(authors) == 2:
            author = f'{authors[0]} ({authors[1]})'
        else:
            author = ', '.join(authors)

        title = soup.select_one('.post-title > h1').text.strip()
        if title.endswith(' Novel'):
            title = title[:-len(' Novel')]

        novel = Novel(
            title=title,
            author=author,
            thumbnail_url=soup.select_one('.summary_image img')['src'],
            synopsis=[p.text.strip() for p in soup.select('.summary__content > hr ~ p')],
            url=url,
        )

        # other metadata
        for item in soup.select('.post-content_item'):
            if item.select_one('.summary-heading').text.strip() == 'Alternative':
                for alt in item.select_one('.summary-content').text.strip().split(', '):
                    if alt != novel.title:
                        novel.metadata.append(Metadata('title', alt, others={'role': 'alt'}))
                break

        for artist in soup.select('.artist-content a'):
            novel.metadata.append(Metadata('contributor', artist.text.strip(), others={'role': 'ill'}))

        for genre in soup.select('.genres-content > a'):
            novel.metadata.append(Metadata('subject', genre.text.strip()))

        short_link = soup.select_one('link[rel="shortlink"]')['href']
        novel_id = parse_qs(urlparse(short_link).query).get('p')[0]
        response = self.session.post(
            'https://novelsite.net/wp-admin/admin-ajax.php',
            data={
                'action': 'manga_get_chapters',
                'manga': novel_id,
            }
        )

        soup = BeautifulSoup(response.content, 'lxml')

        volume = novel.get_default_volume()
        for a in reversed(soup.select('.wp-manga-chapter > a')):
            chapter = Chapter(
                index=len(volume.chapters),
                title=a.text.strip(),
                url=a['href'],
            )

            volume.chapters.append(chapter)

        return novel

    def chapter(self, chapter: Chapter):
        soup = self.get_soup(chapter.url)

        content = soup.select_one('.reading-content')

        # text-left has a better collection of paragraphs...
        # however we are not taking any chances assuming its always there
        text_left = content.select_one('.text-left')
        if text_left:
            content = text_left

        self.clean_contents(content)

        chapter.title = soup.select_one('.breadcrumb > li.active').text.strip(),
        chapter.paragraphs = str(content)
