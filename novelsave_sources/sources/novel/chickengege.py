import datetime

from .source import Source
from ...models import Novel, Chapter, Metadata


class ChickEngege(Source):
    base_urls = ('https://www.chickengege.org',)
    last_updated = datetime.date(2021, 9, 7)

    def novel(self, url: str) -> Novel:
        soup = self.get_soup(url)

        thumbnail_element = soup.select_one('.novelist-cover-image')

        # remove 'synopsis:' from synopsis paragraphs
        soup.select_one('.novelist-align ~ p strong').extract()

        novel = Novel(
            title=soup.select_one('.entry-title').text.strip(),
            thumbnail_url=thumbnail_element['src'] if thumbnail_element else None,
            synopsis=[p.text.strip() for p in soup.select('.novelist-align ~ p')],
            url=url,
        )

        for element in soup.select('.entry-content > div strong'):
            text = element.text.strip()
            if text == 'Original Title:':
                novel.metadata.append(
                    Metadata('title', element.findNext('span').text.strip(), others={'type': 'original'}))
            elif text == 'Translator(s):':
                ul = element.findNext('ul')
                for a in ul.select('li > a'):
                    novel.metadata.append(Metadata('contributor', a.text.strip(), others={'role': 'translator'}))
            elif text == 'Editor(s):':
                ul = element.findNext('ul')
                for a in ul.select('li > a'):
                    novel.metadata.append(Metadata('contributor', a.text.strip(), others={'role': 'editor'}))

        for a in soup.select('a[rel="tag"]'):
            novel.metadata.append(Metadata('subject', a.text.strip()))

        volume = novel.get_default_volume()
        for a in soup.select('#novelList > li > a'):
            chapter = Chapter(
                index=len(volume.chapters),
                title=a.text.strip(),
                url=a['href'],
            )

            volume.chapters.append(chapter)

        return novel

    def chapter(self, chapter: Chapter):
        soup = self.get_soup(chapter.url)

        content = soup.select_one('.entry-wrap .entry-content')
        self.clean_contents(content)

        chapter.title = soup.select_one('.entry-title').text.strip()
        chapter.paragraphs = str(content)
