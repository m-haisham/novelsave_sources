import datetime

from .source import Source
from ...models import Chapter, Novel, Metadata


class DragonTea(Source):
    name = 'Dragon Tea'
    base_urls = ('https://dragontea.ink/',)
    last_updated = datetime.date(2021, 9, 7)

    bad_tags = [
        'noscript', 'script', 'iframe', 'form', 'hr', 'img', 'ins',
        'button', 'input', 'amp-auto-ads', 'pirate',
        'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    ]

    def novel(self, url: str) -> Novel:
        soup = self.get_soup(url)

        novel = Novel(
            title=soup.select_one('.post-title').text.strip(),
            author=soup.select_one('.author-content').text.strip(),
            thumbnail_url=self.to_absolute_url(soup.select_one('.summary_image img')['src'], url),
            synopsis=[p.text.strip() for p in soup.select('.summary__content > p')],
            url=url,
        )

        # other metadata
        for item in soup.select('.post-content_item'):
            key = item.select_one('.summary-heading').text.strip()
            value = item.select_one('.summary-content').text.strip()
            if key == 'Alternative':
                novel.metadata.append(Metadata('title', value, others={'role': 'alt'}))
            elif key == 'Type':
                novel.metadata.append(Metadata('type', value))

        for a in soup.select('.genres-content > a'):
            novel.metadata.append(Metadata('subject', a.text.strip()))

        for a in soup.select('.tags-content > a'):
            novel.metadata.append(Metadata('tag', a.text.strip()))

        artist_content = soup.select_one('.artist-content > a')
        if artist_content:
            novel.metadata.append(Metadata('contributor', artist_content.text.strip(), others={'role': 'ill'}))

        soup = self.get_soup(url.rstrip('/') + '/ajax/chapters/', method='POST')
        volume = novel.get_default_volume()
        for a in reversed(soup.select('.wp-manga-chapter > a')):
            chapter = Chapter(
                index=len(volume.chapters),
                title=a.text.strip(),
                url=self.to_absolute_url(a['href']),
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

        chapter.title = soup.select_one('.breadcrumb > li.active').text.strip()
        chapter.paragraphs = str(content)
