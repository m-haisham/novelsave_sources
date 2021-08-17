from typing import Tuple, List

from .source import Source
from ...models import Chapter, Novel, Metadata


class BoxNovel(Source):
    base_urls = ('https://boxnovel.com',)

    def novel(self, url: str) -> Tuple[Novel, List[Chapter], List[Metadata]]:
        soup = self.soup(url)
        metadata = []

        authors = soup.select('.author-content a')
        if len(authors) == 2:
            author = authors[0].text + ' (' + authors[1].text + ')'
        else:
            author = authors[0].text

        novel = Novel(
            title=''.join(soup.select_one('.post-title h3').find_all(text=True, recursive=False)).strip(),
            author=author.strip(),
            synopsis=soup.select_one('.j_synopsis, #editdescription').text.strip(),
            thumbnail_url=soup.select_one('.summary_image img')['src'],
            url=url,
        )

        for a in soup.select('a[href*="genre"][rel="tag"]'):
            metadata.append(Metadata('subject', a.text.strip()))

        chapters = []
        for i, a in enumerate(reversed(soup.select('ul.main li.wp-manga-chapter a'))):
            chapter = Chapter(
                index=i,
                title=a.text.strip(),
                url=a['href']
            )

            chapters.append(chapter)

        return novel, chapters, metadata

    def chapter(self, chapter: Chapter):
        soup = self.soup(chapter.url)

        contents = soup.select_one('div.text-left')
        for element in contents.select('h1, h2, h3, .code-block, script, .adsbygoogle'):
            element.extract()

        chapter.paragraphs = str(contents)
