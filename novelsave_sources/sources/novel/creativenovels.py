import datetime
import re
from typing import List
from urllib.parse import urlparse, parse_qs

from .source import Source
from ...models import Novel, Chapter, Metadata


class CreativeNovels(Source):
    name = 'Creative Novels'
    base_urls = ('https://creativenovels.com',)
    last_updated = datetime.date(2021, 9, 17)

    def novel(self, url: str) -> Novel:
        soup = self.get_soup(url)

        thumbnail_img = soup.select_one('img.book_cover')

        novel = Novel(
            title=soup.select_one('.x-bar-container > [class*="12"]').text.strip(),
            author=soup.select_one('.x-bar-container > [class*="14"]').text.strip().strip('Author: '),
            thumbnail_url=thumbnail_img.get('src', None) or thumbnail_img.get('data-cfsrc', None),
            synopsis=[p.text.strip() for p in soup.select('.novel_page_synopsis > p')],
            url=url,
        )

        for a in soup.select('.genre_novel > a'):
            novel.metadata.append(Metadata('subject', a.text.strip()))

        for a in soup.select('.suggest_tag > a'):
            novel.metadata.append(Metadata('tag', a.text.strip()))

        novel_id = parse_qs(urlparse(soup.select_one('link[rel="shortlink"]')['href']).query)['p'][0]
        security_key = ''
        for script in soup.select('script'):
            text = script.string
            if not text or 'var chapter_list_summon' not in text:
                continue

            p = re.findall(r'"([^"]+)"', text)
            if p[0] == 'ajaxurl' and p[1] == r'https:\/\/creativenovels.com\/wp-admin\/admin-ajax.php':
                if p[2] == 'security':
                    security_key = p[3]

        response = self.session.post(
            'https://creativenovels.com/wp-admin/admin-ajax.php',
            data=dict(
                action='crn_chapter_list',
                view_id=novel_id,
                s=security_key
            )
        )

        volume = novel.get_default_volume()
        volume.chapters = self.parse_chapter_list(response.content.decode('utf-8'))

        return novel

    def parse_chapter_list(self, content: str) -> List[Chapter]:
        chapters = []

        if not content.startswith('success'):
            return chapters

        content = content[len('success.define.'):]
        for data in content.split('.end_data.'):
            parts = data.split('.data.')
            if len(parts) < 2:
                continue

            chapter = Chapter(
                index=len(chapters),
                title=parts[1],
                url=parts[0],
            )

            chapters.append(chapter)

        return chapters

    def chapter(self, chapter: Chapter):
        soup = self.get_soup(chapter.url)

        bad_selectors = [
            '.announcements_crn', '.support-placement', 'span[style*="color:transparent"]',
            '.count_gloss', '.gloss_fine',
        ]

        content = soup.select_one('article .entry-content')
        for tag in content.select(', '.join(bad_selectors)):
            tag.extract()

        self.clean_contents(content)

        chapter.title = soup.select_one('.entry-title').text.strip()
        chapter.paragraphs = str(content)
