import datetime
import re

from .source import Source
from ...models import Chapter, Novel, Metadata, Asset


class Chrysanthemumgarden(Source):
    name = 'Chrysanthemum Garden'
    base_urls = ('https://chrysanthemumgarden.com/',)
    last_updated = datetime.date(2021, 10, 7)

    bad_tags = [
        'div', 'pirate', 'script',
        'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    ]

    blacklist_patterns = [
        r'^(\s| )+$',  # non-breaking whitespace
    ]

    def __init__(self):
        super(Chrysanthemumgarden, self).__init__()
        self.preserve_attrs += ['class']

    def novel(self, url: str) -> Novel:
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

        novel.assets.append(
            Asset(
                name='OpenSans-Jumbld2',
                url='https://chrysanthemumgarden.com/wp-content/themes/chrys-garden-generatepress/resources/css/fonts'
                    '/OpenSans-Jumbld2.woff2',
                mimetype='font/woff2',
                scope='.jum',
            )
        )

        return novel

    def chapter(self, chapter: Chapter):
        soup = self.get_soup(chapter.url)

        content = soup.select_one('#novel-content')
        self.clean_contents(content)

        # only keep the .jum class
        for element in content.select('[class]'):
            if 'jum' in element['class']:
                element['class'] = 'jum'
            else:
                del element['class']

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

        super(Chrysanthemumgarden, self).clean_element(element)
