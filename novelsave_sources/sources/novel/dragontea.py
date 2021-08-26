from typing import List, Tuple
from urllib.parse import urlparse, parse_qs

from bs4 import BeautifulSoup

from .source import Source
from ...models import Chapter, Novel, Metadata


class DragonTea(Source):
    name = 'Dragon Tea'
    base_urls = ('https://dragontea.ink/',)

    bad_tags = [
        'noscript', 'script', 'iframe', 'form', 'hr', 'img', 'ins',
        'button', 'input', 'amp-auto-ads', 'pirate',
        'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    ]

    def novel(self, url: str) -> Tuple[Novel, List[Chapter], List[Metadata]]:
        soup = self.soup(url)

        summary_paragraphs = [p.text.strip() for p in soup.select('.summary__content > p')]

        novel = Novel(
            title=soup.select_one('.post-title').text.strip(),
            author=soup.select_one('.author-content').text.strip(),
            thumbnail_url=soup.select_one('.summary_image img')['src'],
            synopsis='\n'.join(summary_paragraphs),
            url=url,
        )

        # other metadata
        metadata = []
        for item in soup.select('.post-content_item'):
            key = item.select_one('.summary-heading').text.strip()
            value = item.select_one('.summary-content').text.strip()
            if key == 'Alternative':
                metadata.append(Metadata('title', value, others={'role': 'alt'}))
            elif key == 'Type':
                metadata.append(Metadata('type', value))

        for a in soup.select('.genres-content > a'):
            metadata.append(Metadata('subject', a.text.strip()))

        for a in soup.select('.tags-content > a'):
            metadata.append(Metadata('tag', a.text.strip()))

        artist_content = soup.select_one('.artist-content > a')
        if artist_content:
            metadata.append(Metadata('contributor', artist_content.text.strip(),
                                     others={'role': 'ill', 'link': artist_content['href']}))

        short_link = soup.select_one('[rel="shortlink"]')['href']
        novel_id = int(parse_qs(urlparse(short_link).query)['p'][0])
        response = self.session.post(
            'https://dragontea.ink/wp-admin/admin-ajax.php',
            data={
                'action': 'manga_get_chapters',
                'manga': novel_id,
            }
        )

        soup = BeautifulSoup(response.content, 'lxml')

        chapters = []
        for a in reversed(soup.select('.wp-manga-chapter > a')):
            chapter = Chapter(
                index=len(chapters),
                title=a.text.strip(),
                url=a['href'],
            )

            chapters.append(chapter)

        return novel, chapters, metadata

    def chapter(self, chapter: Chapter):
        soup = self.soup(chapter.url)

        content = soup.select_one('.reading-content')

        # text-left has a better collection of paragraphs...
        # however we are not taking any chances assuming its always there
        text_left = content.select_one('.text-left')
        if text_left:
            content = text_left

        self.clean_contents(content)

        chapter.title = soup.select_one('.breadcrumb > li.active').text.strip()
        chapter.paragraphs = str(content)
