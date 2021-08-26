import re
from typing import Tuple, List
from urllib.parse import urlparse, parse_qs

from .source import Source
from ...models import Novel, Chapter, Metadata


class CreativeNovels(Source):
    name = 'Creative Novels'
    base_urls = ('https://creativenovels.com',)

    def novel(self, url: str) -> Tuple[Novel, List[Chapter], List[Metadata]]:
        soup = self.soup(url)
        metadata = []

        novel = Novel(
            title=soup.select_one('.x-bar-container > [class*="12"]').text.strip(),
            author=soup.select_one('.x-bar-container > [class*="14"]').text.strip().strip('Author: '),
            thumbnail_url=soup.select_one('.x-content-area > img')['src'],
            synopsis='\n'.join([p.text.strip() for p in soup.select('.novel_page_synopsis > p')]),
            url=url,
        )

        for a in soup.select('.suggest_tag > a'):
            metadata.append(Metadata('subject', a.text.strip()))

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

        chapters = self.parse_chapter_list(response.content.decode('utf-8'))

        return novel, chapters, metadata

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
        soup = self.soup(chapter.url)

        content = soup.select_one('article .entry-content')
        for tag in content.select('.announcements_crn, .support-placement, span[style*="color:transparent"]'):
            tag.extract()

        self.clean_contents(content)

        chapter.title = soup.select_one('.entry-title').text.strip()
        chapter.paragraphs = str(content)
