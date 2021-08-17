from typing import List, Tuple

from bs4 import BeautifulSoup

from .source import Source
from ...models import Chapter, Novel, Metadata


class NovelSite(Source):
    base_urls = ('https://novelsite.net',)

    bad_tags = [
        'noscript', 'script', 'iframe', 'form', 'hr', 'img', 'ins',
        'button', 'input', 'amp-auto-ads', 'pirate',
        'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    ]

    def novel(self, url: str) -> Tuple[Novel, List[Chapter], List[Metadata]]:
        soup = self.soup(url)
        metadata = []

        authors = [a for a in soup.select('.author-content > a')]

        novel = Novel(
            title=soup.select_one('.post-title > h1').text.strip().rstrip(' Novel'),
            author=authors[0].text.strip(),
            thumbnail_url=soup.select_one('.summary_image img')['src'],
            synopsis=soup.select_one('.summary__content > hr + p').text.strip(),
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
            metadata.append(Metadata('contributor', author.text.strip(),
                                     others={'role': 'aut', 'link': author['href']}))

        artists = soup.select('.artist-content a')
        for artist in artists:
            metadata.append(Metadata('contributor', artist.text.strip(),
                                     others={'role': 'ill', 'link': artist['href']}))

        genres = soup.select('.genres-content > a')
        for genre in genres:
            metadata.append(Metadata('subject', genre.text.strip()))

        novel_id = soup.select_one('.rating-post-id_')['value']
        response = self.session.post(
            'https://novelsite.net/wp-admin/admin-ajax.php',
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

        chapter.title = soup.select_one('.breadcrumb >li.active').text.strip(),
        chapter.paragraphs = str(content)
