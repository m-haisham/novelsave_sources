import datetime

from .source import Source
from ...models import Chapter, Novel, Metadata


class NovelPassion(Source):
    base_urls = ('https://www.novelpassion.com',)
    last_updated = datetime.date(2021, 9, 4)

    def novel(self, url: str) -> Novel:
        soup = self.get_soup(url)

        authors = [a.text.strip() for a in soup.select('.dns .stq[href*="author"]')]
        synopsis_paragraphs = [p.text.strip() for p in soup.select('.j_synopsis p')]

        novel = Novel(
            title=soup.select_one('.psn h2.ddm').text.strip(),
            author=', '.join(authors),
            thumbnail_url=self.base_urls[0] + soup.select_one('.g_thumb img')['src'],
            synopsis=synopsis_paragraphs,
            url=url,
        )

        for a in soup.select('.dns .stq[href*="category"]'):
            novel.metadata.append(Metadata('subject', a.text.strip()))

        volume = novel.get_default_volume()
        for i, a in enumerate(reversed(soup.select('.content-list a'))):
            chapter = Chapter(
                index=i,
                title=a.select_one('span').text.strip(),
                url=self.base_urls[0] + a['href'],
            )

            volume.chapters.append(chapter)

        return novel

    def chapter(self, chapter: Chapter):
        soup = self.get_soup(chapter.url)

        content = soup.select_one('.cha-words')
        self.clean_contents(content)

        chapter.title = soup.select_one('h2.dac').text.strip()
        chapter.paragraphs = str(content)
