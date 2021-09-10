import datetime

from .source import Source
from ...models import Chapter, Novel, Metadata


class BoxNovel(Source):
    base_urls = ('https://boxnovel.com',)
    last_updated = datetime.date(2021, 9, 7)

    def novel(self, url: str) -> Novel:
        soup = self.get_soup(url)

        authors = soup.select('.author-content a')
        if len(authors) == 2:
            author = authors[0].text.strip() + ' (' + authors[1].text.strip() + ')'
        else:
            author = authors[0].text.strip()

        novel = Novel(
            title=soup.select_one('.breadcrumb > li:last-child').text.strip(),
            author=author,
            synopsis=[t.strip() for t in soup.select_one('.j_synopsis, #editdescription').text.splitlines() if t.strip()],
            thumbnail_url=soup.select_one('.summary_image img')['src'],
            url=url,
        )

        for a in soup.select('a[href*="genre"][rel="tag"]'):
            novel.metadata.append(Metadata('subject', a.text.strip()))

        soup = self.get_soup(url.rstrip('/') + '/ajax/chapters', 'POST')
        volume = novel.get_default_volume()
        for i, a in enumerate(reversed(soup.select('li.wp-manga-chapter a'))):
            chapter = Chapter(
                index=i,
                title=a.text.strip(),
                url=a['href']
            )

            volume.chapters.append(chapter)

        return novel

    def chapter(self, chapter: Chapter):
        soup = self.get_soup(chapter.url)

        contents = soup.select_one('div.text-left')
        for element in contents.select('h1, h2, h3, .code-block, script, .adsbygoogle'):
            element.extract()

        chapter.paragraphs = str(contents)
