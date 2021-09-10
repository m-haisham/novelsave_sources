import datetime

from .source import Source
from ...models import Chapter, Novel, Metadata


class NovelsRock(Source):
    name = 'Novels Rock'
    base_urls = ('https://novelsrock.com',)
    last_updated = datetime.date(2021, 9, 4)

    def novel(self, url: str) -> Novel:
        soup = self.get_soup(url)

        novel = Novel(
            title=soup.select_one('.breadcrumb > li:last-child').text.strip(),
            author=', '.join([a.text.strip() for a in soup.select('.author-content > a')]),
            thumbnail_url=soup.select_one('.summary_image img')['src'],
            synopsis=[str(p).strip() for p in soup.select_one('.summary__content').find_all(text=True, recursive=False)],
            url=url,
        )

        for a in soup.select('.summary_content_wrap a[href*="genre"]'):
            novel.metadata.append(Metadata('subject', a.text.strip()))

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

        contents = soup.select('div.reading-content p')

        body = []
        for p in contents:
            for ad in p.select('h3, .code-block, .adsense-code'):
                ad.decompose()
            body.append(str(p))

            chapter.paragraphs = ''.join(body)
