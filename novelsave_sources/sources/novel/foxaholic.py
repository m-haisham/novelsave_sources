import datetime
from typing import List, Tuple

from bs4 import BeautifulSoup

from .source import Source
from ...models import Chapter, Volume, Novel, Metadata


class Foxaholic(Source):
    base_urls = ('https://www.foxaholic.com',)
    last_updated = datetime.date(2021, 9, 3)

    bad_tags = [
        'noscript', 'script', 'iframe', 'form', 'hr', 'img', 'ins',
        'button', 'input', 'amp-auto-ads', 'pirate',
        'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    ]

    blacklist_patterns = [
        r'^[\W\D]*(volume|chapter)[\W\D]+\d+[\W\D]*$',
        r'^ $',  # non-breaking whitespace
    ]

    def novel(self, url: str) -> Novel:
        soup = self.get_soup(url)

        hot = soup.select_one('.post-title .hot')
        if hot:
            hot.extract()

        authors = soup.select('.author-content > a')
        synopsis_paras = soup.select('.summary__content > p')

        novel = Novel(
            title=soup.select_one('.post-title').text.strip(),
            author=authors[0].text.strip(),
            thumbnail_url=soup.select_one('.summary_image img')['src'],
            synopsis=[p.text.strip() for p in synopsis_paras],
            url=url,
        )

        # other metadata
        for item in soup.select('.post-content_item'):
            if item.select_one('.summary-heading').text.strip() == 'Alternative':
                for alt in item.select_one('.summary-content').text.strip().split(', '):
                    if alt != novel.title:
                        novel.metadata.append(Metadata('title', alt, others={'role': 'alt'}))
                break

        for author in authors[1:]:
            novel.metadata.append(Metadata('contributor', author.text.strip(), others={'role': 'aut'}))

        for artist in soup.select('.artist-content a'):
            novel.metadata.append(Metadata('contributor', artist.text.strip()))

        for genre in soup.select('.genres-content > a'):
            novel.metadata.append(Metadata('subject', genre.text.strip()))

        for tag in soup.select('.tags-content > a'):
            novel.metadata.append(Metadata('tag', tag.text.strip()))

        novel_id = soup.select_one('.wp-manga-action-button')['data-post']
        response = self.session.post(
            'https://www.foxaholic.com/wp-admin/admin-ajax.php',
            data={
                'action': 'manga_get_chapters',
                'manga': novel_id,
            }
        )

        soup = BeautifulSoup(response.content, 'lxml')

        volume = Volume.default()
        novel.volumes.append(volume)
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

        for hidden in soup.select('[class*="foxaholic-publift"]'):
            hidden.extract()

        self.clean_contents(content)

        chapter.title = soup.select_one('.breadcrumb > li.active').text.strip()
        chapter.paragraphs = str(content)
