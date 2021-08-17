from typing import Tuple, List

from .source import Source
from ...models import Novel, Chapter, Metadata


class WuxiaOnline(Source):
    name = 'WuxiaWorld.online'
    base_urls = ('https://wuxiaworld.online',)

    def novel(self, url: str) -> Tuple[Novel, List[Chapter], List[Metadata]]:
        soup = self.soup(url)

        synopsis_elements = soup.select_one('#noidungm').find_all(text=True, recursive=False)

        novel = Novel(
            title=soup.select_one('h1.entry-title').text.strip(),
            author=soup.select_one('a[href*="author"]').text.strip(),
            thumbnail_url=self.base_urls[0] + soup.select_one('.info_image img')['src'],
            synopsis='\n'.join([str(element) for element in synopsis_elements]),
            url=url,
        )

        chapters = []
        for a in reversed(soup.select('.chapter-list > .row a')):
            chapter = Chapter(
                index=len(chapters),
                title=a.text.strip(),
                url=a['href']
            )

            chapters.append(chapter)

        return novel, chapters, []

    def chapter(self, chapter: Chapter):
        soup = self.soup(chapter.url)

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
