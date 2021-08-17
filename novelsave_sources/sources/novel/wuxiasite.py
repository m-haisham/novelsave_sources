from typing import List, Tuple

from .source import Source
from ...models import Chapter, Novel, Metadata


class WuxiaSite(Source):
    name = 'WuxiaWorld.site'
    base_urls = ('https://wuxiaworld.site',)

    def novel(self, url: str) -> Tuple[Novel, List[Chapter], List[Metadata]]:
        soup = self.soup(url)
        metadata = []

        # ---- info ----

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
            thumbnail_url=soup.select_one('.summary_image a img')['src'],
            synopsis='\n'.join(p.text.strip() for p in soup.select('.summary__content > p')),
            url=url,
        )

        for a in soup.select('a[href*="genre"][rel="tag"]'):
            metadata.append(Metadata('subject', a.text.strip()))

        # ---- chapters ----

        chapters = []
        for a in reversed(soup.select('ul.main li.wp-manga-chapter a')):
            index = len(chapters)
            chapter = Chapter(
                index=index,
                title=a.text.strip() or f'Chapter {index}',
                url=a['href'],
            )

            chapters.append(chapter)

        return novel, chapters, metadata

    def chapter(self, chapter: Chapter):
        soup = self.soup(chapter.url)

        contents = soup.select('.text-left p, .cha-words p')
        body = [str(p) for p in contents if p.text.strip()]

        chapter.paragraphs = ''.join(body)
