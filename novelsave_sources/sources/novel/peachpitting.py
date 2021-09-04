import datetime

from .source import Source
from ...models import Chapter, Novel, Metadata


class PeachPitting(Source):
    name = 'Peach Pits'
    base_urls = ('https://peachpitting.com',)
    last_updated = datetime.date(2021, 9, 4)

    def novel(self, url: str) -> Novel:
        soup = self.get_soup(url)

        details_parent, synopsis_parent, *_ = soup.select('.elementor-text-editor')

        novel = Novel(
            title=soup.select_one('h3.elementor-heading-title').text.strip(),
            thumbnail_url=soup.select_one('.elementor-image img')['src'],
            synopsis=[p.text.strip() for p in synopsis_parent.select('p')],
            url=url,
        )

        for p in details_parent.select('p'):
            text = p.text.strip()
            if text.startswith('Author: '):
                novel.author = text.strip('Author: ')
            elif text.startswith('Tags: '):
                for text in text.strip('Tags: ').split(','):
                    novel.metadata.append(Metadata('subject', text.strip()))

        # other contributors
        for a in soup.select('.pp-multiple-authors-wrapper .author'):
            novel.metadata.append(Metadata('contributor', a.text.strip()))

        volume = novel.get_default_volume()
        for a in soup.select('.pt-cv-page > div a'):
            chapter = Chapter(
                index=len(volume.chapters),
                title=a.text.strip(),
                url=a['href'],
            )

            volume.chapters.append(chapter)

        return novel

    def chapter(self, chapter: Chapter):
        soup = self.get_soup(chapter.url)

        content = soup.select_one('#wtr-content')

        # remove ads
        for div in content.select('.ad-section'):
            div.extract()

        self.clean_contents(content)

        chapter.title = soup.select_one('.post-title').text.strip()
        chapter.paragraphs = str(content)
