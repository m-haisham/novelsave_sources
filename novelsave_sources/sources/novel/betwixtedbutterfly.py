import datetime
from typing import List, Tuple

from bs4 import BeautifulSoup

from .source import Source
from ...models import Chapter, Volume, Novel, Metadata
from ...exceptions import ChapterException


class BetwixtedButterfly(Source):
    name = 'Betwixted Butterfly'
    base_urls = ('https://betwixtedbutterfly.com',)
    last_updated = datetime.date(2021, 9, 3)

    bad_tags = [
        'noscript', 'script', 'iframe', 'form', 'img', 'ins',
        'button', 'input', 'amp-auto-ads', 'pirate',
        'nav', 'h1', 'h2',
    ]

    def novel(self, url: str) -> Tuple[Novel, List[Chapter], List[Metadata]]:
        soup = self.get_soup(url)

        details_parent, synopsis_parent, *_ = soup.select('.elementor-text-editor')

        author = None
        for p in details_parent.select('p'):
            if p.text.startswith('Author: '):
                author = p.text.strip('Author: ')
                break

        novel = Novel(
            title=soup.select_one('h2.elementor-heading-title').text.strip(),
            author=author,
            synopsis=[p.text.strip() for p in synopsis_parent.select('p')],
            thumbnail_url=soup.select_one('.elementor-image img')['src'],
            url=url,
        )

        # tags
        for a in soup.select('a.elementor-button'):
            novel.metadata.append(Metadata('subject', a.text.strip()))

        volume = Volume.default()
        novel.volumes.append(volume)
        for a in soup.select('.elementor-tab-content > p a'):
            chapter = Chapter(
                index=len(volume.chapters),
                title=a.text.strip(),
                url=a['href']
            )

            volume.chapters.append(chapter)

        return novel

    def chapter(self, chapter: Chapter):
        soup = self.get_soup(chapter.url)

        elements = soup.select(".entry-inner section .elementor-element:not(.elementor-widget-button, "
                               ".elementor-column)")
        if elements:
            content = BeautifulSoup(f'<div>{"".join([str(element) for element in elements])}</div>', 'lxml').select_one('div')
        else:
            content = soup.select_one('.entry-inner')

        # this source lists chapters that aren't completed/translated in table of contents
        # links of said chapter are redirected to another url that indicates the lack of the chapter
        if content is None:
            raise ChapterException('Absent', f'"{chapter}" redirected to placeholder')

        # remove navigation buttons
        for button in content.select('.elementor-widget-button'):
            button.extract()

        # wp-block-columns -> navigation
        # code-block -> ads
        for div in content.select('.wp-block-columns, .code-block'):
            div.extract()

        self.clean_contents(content)

        chapter.paragraphs = str(content)
