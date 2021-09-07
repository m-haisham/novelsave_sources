import datetime

from .source import Source
from ...models import Chapter, Novel, Metadata


class NovelFull(Source):
    name = 'NovelFull'
    base_urls = ('https://novelfull.com',)
    last_updated = datetime.date(2021, 9, 7)

    bad_tags = [
        'noscript', 'script', 'iframe', 'form', 'hr', 'img', 'ins',
        'button', 'input', 'amp-auto-ads', 'pirate',
        'h1', 'h2', 'h3'
    ]

    blacklist_patterns = [
        r'^\s*Translator:',
        r'^\s*Editor:',
        r'^\s*Atlas Studios',
        r'Read more chapter on NovelFull',
        r'full thich ung',
        r'If you find any errors \( broken links.*let us know < report chapter >',
    ]

    def novel(self, url: str) -> Novel:
        soup = self.get_soup(url)

        image_element = soup.select_one('.info-holder .book img')

        authors = [a.text.strip() for a in soup.select('.info a[href*="/author"]')]
        if len(authors) == 2:
            author = f'{authors[0]} ({authors[1]})'
        else:
            author = ', '.join(authors)

        novel = Novel(
            title=image_element['alt'],
            author=author,
            thumbnail_url=self.base_urls[0] + image_element['src'],
            synopsis=[p.text.strip() for p in soup.select('.desc-text > p')],
            url=url,
        )

        for a in soup.select('.info a[href*="/genre"]'):
            novel.metadata.append(Metadata('subject', a.text.strip()))

        soup.select_one('.info').smooth()
        for div in soup.select('.info > div'):
            heading = div.select_one('h3').text.strip()
            value = div.find(text=True, recursive=False)
            if heading == 'Alternative names:':
                titles = value.split(', ')
                for title in titles:
                    novel.metadata.append(Metadata('title', title, others={'role': 'alt'}))
            elif heading == 'Source:':
                novel.metadata.append(Metadata('publisher', value))
            elif heading == 'Status:':
                novel.metadata.append(Metadata('status', div.select_one('a').text.strip()))

        last_pagination = soup.select_one('#list-chapter .pagination .last a')
        page_count = int(
            last_pagination['data-page']) if last_pagination else 0

        volume = novel.get_default_volume()
        for page in range(1, page_count + 2):
            self.parse_chapter_list(volume, url, page)

        return novel

    def parse_chapter_list(self, volume, novel_url, page):
        url = f'{novel_url.rstrip("/")}?page={page}&per-page=50'
        soup = self.get_soup(url)

        for a in soup.select('ul.list-chapter li a'):
            chapter = Chapter(
                index=len(volume.chapters),
                title=a['title'].strip(),
                url=self.base_urls[0] + a['href'],
            )

            volume.chapters.append(chapter)

    def chapter(self, chapter: Chapter):
        soup = self.get_soup(chapter.url)

        content = soup.select_one('div#chapter-content')

        self.clean_contents(content)
        for ads in content.select('h3, h2, .adsbygoogle, script, ins, .ads, .ads-holder'):
            ads.extract()

        chapter.title = soup.select_one('.chapter-text').find(text=True, recursive=False).strip()
        chapter.paragraphs = str(content)
