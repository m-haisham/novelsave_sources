import datetime
import re
from typing import List, Tuple

from .source import Source
from ...models import Chapter, Novel, Metadata


class Chrysanthemumgarden(Source):
    name = 'Chrysanthemum Garden'
    base_urls = ('https://chrysanthemumgarden.com/',)
    last_updated = datetime.date(2021, 9, 7)

    bad_tags = [
        'div', 'pirate', 'script',
        'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    ]

    blacklist_patterns = [
        r'^(\s| )+$',  # non-breaking whitespace
    ]

    def novel(self, url: str) -> Tuple[Novel, List[Chapter], List[Metadata]]:
        soup = self.get_soup(url)

        synopsis = []
        synopsis_elements = soup.select('.entry-content > p, hr')
        for element in synopsis_elements:
            if element.tag == 'hr':
                break

            synopsis.append(element.text.strip())

        novel = Novel(
            title=soup.select_one('.novel-title').find(text=True).strip(),
            author=soup.select_one('.author-name > a').text.strip(),
            synopsis=synopsis,
            thumbnail_url=soup.select_one('.novel-cover img')['src'],
            url=url,
        )

        raw_title = soup.select_one('.novel-raw-title')
        if raw_title:
            novel.metadata.append(Metadata('title', raw_title.text.strip(), others={'role': 'alt'}))

        for a in soup.select('.series-tag'):
            novel.metadata.append(Metadata('subject', a.text.strip()))

        volume = novel.get_default_volume()
        for i, a in enumerate(soup.select('.chapter-item > a')):
            chapter = Chapter(
                index=i,
                title=a.text.strip(),
                url=a['href'],
            )

            volume.chapters.append(chapter)

        return novel

    def chapter(self, chapter: Chapter):
        soup = self.get_soup(chapter.url)

        content = soup.select_one('#novel-content')
        self.clean_contents(content)

        chapter.title = soup.select_one('.chapter-title').text.strip()
        chapter.paragraphs = str(content)

    def clean_element(self, element):

        # this removes hidden elements
        try:
            if re.match(r'(height:\s*1px|width:\s*0)', element['style'], flags=re.IGNORECASE):
                element.extract()
                return
        except KeyError:
            pass

        if 'class' in element.attrs and 'jum' in element['class']:
            self.reorder_text(element)

        super(Chrysanthemumgarden, self).clean_element(element)

    def reorder_text(self, element):
        text = ''
        for char in element.text:
            try:
                text += self.jumble_map[char]
            except KeyError:
                text += char

        element.string = text

    jumble_map = {'j': 'a', 'y': 'b', 'm': 'c', 'v': 'd', 'f': 'e', 'o': 'f', 'u': 'g', 't': 'h', 'l': 'i', 'p': 'j',
                  'x': 'k', 'i': 'l', 'w': 'm', 'c': 'n', 'b': 'o', 'q': 'p', 'd': 'q', 'g': 'r', 'r': 's', 'a': 't',
                  'e': 'u', 'n': 'v', 'k': 'w', 'z': 'x', 's': 'y', 'h': 'z', 'C': 'A', 'D': 'B', 'J': 'C', 'G': 'D',
                  'S': 'E', 'M': 'F', 'X': 'G', 'L': 'H', 'P': 'I', 'A': 'J', 'B': 'K', 'O': 'L', 'Z': 'M', 'R': 'N',
                  'Y': 'O', 'U': 'P', 'H': 'Q', 'E': 'R', 'V': 'S', 'K': 'T', 'F': 'U', 'N': 'V', 'Q': 'W', 'W': 'X',
                  'T': 'Y', 'I': 'Z'}
