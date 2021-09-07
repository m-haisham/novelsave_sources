from typing import List, Tuple
from urllib.parse import urlparse

from .source import Source
from ...models import Chapter, Novel, Metadata


class FanFiction(Source):
    base_urls = ('https://www.fanfiction.net',)
    rejected = 'Has cloudflare bot protection'

    def novel(self, url: str) -> Tuple[Novel, List[Chapter], List[Metadata]]:
        soup = self.get_soup(url)
        metadata = []

        cover = None
        image_element = soup.select_one('#profile_top img.cimage')
        if image_element:
            cover = f'https:{image_element["src"]}'

        novel = Novel(
            title=soup.select_one('#profile_top b.xcontrast_txt, #content b').text.strip(),
            author=soup.select_one('#profile_top, #content').select_one('a[href*="/u/"]').text.strip(),
            synopsis=soup.select_one('#profile_top > div').text.strip(),
            thumbnail_url=cover,
            url=url,
        )

        # metadata
        pre_story_links = soup.select('#pre_story_links a')
        if len(pre_story_links) == 2:
            metadata.append(Metadata(
                namespace='fanfiction',
                name=pre_story_links[0].text.strip(),
                value=pre_story_links[1].text.strip(),
            ))
        else:
            metadata.append(Metadata(
                namespace='fanfiction',
                name='Crossover',
                value=pre_story_links[0].text.rstrip(' Crossover'),
            ))

        id_ = urlparse(url).path.split('/')[2]

        chapters = []
        chapter_select = soup.select_one('#chap_select, select#jump')
        if chapter_select:
            # multi chapter fan-fictions
            for i, option in enumerate(chapter_select.select('option')):
                chapter = Chapter(
                    index=i,
                    title=option.text.strip(),
                    url=f'https://www.fanfiction.net/s/{id_}/{option["value"]}'
                )

                chapters.append(chapter)
        else:
            # single chapter fan-fictions
            chapters.append(
                Chapter(
                    index=0,
                    title=novel.title,
                    url=url,
                )
            )

        return novel, chapters, metadata

    def chapter(self, chapter: Chapter):
        soup = self.get_soup(chapter.url)

        chapter_select = soup.select_one('#chap_select, select#jump')
        if chapter_select:
            title = chapter_select.find('option', selected=True).text.strip()
        else:
            title = soup.select_one('#profile_top b.xcontrast_txt, #content b').text.strip()

        chapter.title = title
        chapter.paragraphs = str(soup.select_one('#storytext, #storycontent'))
