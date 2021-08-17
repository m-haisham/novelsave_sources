from typing import List, Tuple

from bs4 import BeautifulSoup

from .source import Source
from ...models import Chapter, Novel, Metadata


class Foxaholic(Source):
    base_urls = ('https://foxaholic.com/',)

    bad_tags = [
        'noscript', 'script', 'iframe', 'form', 'hr', 'img', 'ins',
        'button', 'input', 'amp-auto-ads', 'pirate',
        'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    ]

    blacklist_patterns = [
        r'^[\W\D]*(volume|chapter)[\W\D]+\d+[\W\D]*$',
        r'^ $',  # non-breaking whitespace
    ]

    def novel(self, url: str) -> Tuple[Novel, List[Chapter], List[Metadata]]:
        soup = self.soup(url)
        metadata = []

        authors = soup.select('.author-content > a')
        synopsis_paras = soup.select('.summary__content > p')

        novel = Novel(
            title=soup.select_one('.post-title').text.strip(),
            author=authors[0].text.strip(),
            thumbnail_url=soup.select_one('.summary_image img')['src'],
            synopsis='\n'.join((p.text.strip() for p in synopsis_paras)),
            url=url,
        )

        # other metadata
        for item in soup.select('.post-content_item'):
            if item.select_one('.summary-heading').text.strip() == 'Alternative':
                for alt in item.select_one('.summary-content').text.strip().split(', '):
                    if alt != novel.title:
                        metadata.append(Metadata('title', alt, others={'role': 'alt'}))
                break

        for author in authors[1:]:
            metadata.append(Metadata('contributor', author.text.strip(), others={'role': 'aut', 'link': author['href']}))

        artists = soup.select('.artist-content a')
        for artist in artists:
            metadata.append(Metadata('contributor', artist.text.strip(), others={'link': artist['href']}))

        genres = soup.select('.genres-content > a')
        for genre in genres:
            metadata.append(Metadata('subject', genre.text.strip()))

        novel_id = soup.select_one('.wp-manga-action-button')['data-post']
        response = self.session.post(
            'https://foxaholic.com/wp-admin/admin-ajax.php',
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
