import datetime

from .source import Source
from ...models import Novel, Chapter


class WuxiaOnline(Source):
    name = 'WuxiaWorld.online'
    base_urls = ('https://wuxiaworld.online',)
    last_updated = datetime.date(2021, 9, 7)

    def novel(self, url: str) -> Novel:
        soup = self.get_soup(url)

        synopsis = []
        for element in soup.select('#noidungm > *'):
            if element.name == 'hr':
                break
            elif element.name == 'p':
                if 'style' in element.attrs:
                    continue

                synopsis.append(element.text.strip())

        novel = Novel(
            title=soup.select_one('h1.entry-title').text.strip(),
            thumbnail_url=self.base_urls[0] + soup.select_one('.info_image img')['src'],
            synopsis=synopsis,
            url=url,
        )

        author_element = soup.select_one('a[href*="author"]')
        if author_element:
            novel.author = author_element.text.strip()

        volume = novel.get_default_volume()
        for a in reversed(soup.select('.chapter-list > .row a')):
            chapter = Chapter(
                index=len(volume.chapters),
                title=a.text.strip(),
                url=a['href']
            )

            volume.chapters.append(chapter)

        return novel

    def chapter(self, chapter: Chapter):
        soup = self.get_soup(chapter.url)

        content = soup.select_one('#list_chapter .content-area')

        for h2 in content.select('h2[style="font-weight:bold"]'):
            h2.extract()

        for hidden in content.select('[style="display:none"]'):
            hidden.extract()

        first_element = next(content.children)
        if first_element.name == 'br':
            first_element.extract()

        self.clean_contents(content)

        chapter.paragraphs = str(content)

    def clean_element(self, element):

        try:
            # hidden anti-scraping content
            if 'display:none' in element['style']:
                element.extract()
                return
        except KeyError:
            pass

        try:
            if element.name == 'h2' and 'font-weight:bold' in element['style']:
                next_sibling = element.nextSibling()
                if next_sibling.name == 'br':
                    next_sibling.extract()

                element.extract()
                return
        except KeyError:
            pass

        super(WuxiaOnline, self).clean_element(element)
