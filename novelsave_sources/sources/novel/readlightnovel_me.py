import datetime
import re
import unicodedata

from .source import Source
from ...models import Novel, Chapter, Metadata


class ReadLightNovel(Source):
    name = 'Read Light Novel'
    base_urls = ('https://www.readlightnovel.me',)
    last_updated = datetime.date(2021, 9, 7)

    def novel(self, url: str) -> Novel:
        soup = self.get_soup(url)

        novel = Novel(
            title=soup.select_one('.block-title h1').text.strip(),
            author=soup.select_one("a[href*=author]").text.strip(),
            synopsis=[p.text.strip() for p in soup.select('.novel-right .novel-detail-item .novel-detail-body > p')],
            thumbnail_url=soup.select_one('.novel-cover img')['src'],
            url=url
        )

        for a in soup.select('.novel-detail-item.color-gray a'):
            novel.metadata.append(Metadata('title', a.text.strip(), others={'role': 'alt'}))

        for a in soup.select('.novel-details a[href*="category"]'):
            novel.metadata.append(Metadata('subject', a.text.strip()))

        for a in soup.select('.novel-details a[href*="tags"]'):
            novel.metadata.append(Metadata('tag', a.text.strip()))

        volume = novel.get_default_volume()
        for a in soup.select('.chapters .chapter-chs li a'):
            chapter = Chapter(
                index=len(volume.chapters),
                title=a.text.strip(),
                url=a['href'],
            )

            volume.chapters.append(chapter)

        return novel

    def chapter(self, chapter: Chapter):
        soup = self.get_soup(chapter.url)

        content = soup.find('div', {'class': 'chapter-content3'}).find('div', {'class': 'desc'})

        title_element = content.find('h3')

        title = None
        if title_element is not None:
            # title can have some unicode characters in them
            title = unicodedata.normalize("NFKD", title_element.text)

        # paragraphs
        paragraphs = []

        if content.find('p') is None:
            # no <p> elements
            for text in content.find_all(text=True, recursive=False):
                paragraphs.append(text)
        else:
            para_elements = content.find_all('p', recursive=False)
            for element in para_elements:
                text = element.text.strip()
                paragraphs.append(text)

        # fixing the formatting issue
        for i in range(len(paragraphs)):
            paragraphs[i] = re.sub(r' \. ?', '. ', paragraphs[i]).strip()

        chapter.title = title
        chapter.paragraphs = paragraphs
