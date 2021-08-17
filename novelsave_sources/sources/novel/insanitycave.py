import re
from typing import List, Tuple

from .source import Source
from ...models import Chapter, Novel, Metadata


class InsanityCave(Source):
    name = 'Insanity Cave'
    base_urls = ('https://insanitycave.poetry.blog',)

    novel_author_regex = re.compile(r'written by(.+)\.')
    chapter_title_regex = re.compile(r'chapter[  ]([0-9]+)[  ]*.[  ](.+)', flags=re.IGNORECASE)

    def novel(self, url: str) -> Tuple[Novel, List[Chapter], List[Metadata]]:
        soup = self.soup(url)

        entry_content = soup.find('div', {'class': 'entry-content'})
        title_text = entry_content.find('p').text.strip()

        novel = Novel(
            title=soup.find('div', {'class': 'title-block'}).text.strip(),
            author=self.novel_author_regex.search(title_text).group(1).strip(),
            thumbnail_url=soup.find('div', {'class': 'wp-block-image'}).find('img')['src'],
            url=url,
        )

        chapters = []
        for i, a in enumerate(entry_content.find_all('a')):

            result = self.chapter_title_regex.search(a.text.strip())

            if not result or len(result.groups()) < 2:
                continue

            chapter = Chapter(
                index=i,
                no=int(result.group(1)),
                title=result.group(2).strip(),
                url=a['href']
            )

            chapters.append(chapter)

        return novel, chapters, []

    def chapter(self, chapter: Chapter):
        soup = self.soup(chapter.url)

        result = self.chapter_title_regex.search(soup.find('div', {'class': 'title-block'}).text.strip())
        if not result or len(result.groups()) < 2:
            raise Exception('Invalid Schema: title')

        entry_content = soup.find('div', {'class': 'entry-content'})

        paras = []
        for p in entry_content.find_all('p'):
            para = p.text.strip()
            if not para:
                continue
            elif 'Previous Chapter |' in para:
                continue
            elif '| Next Chapter' in para:
                continue
            else:
                paras.append(para)

        chapter.title = result.group(2).strip()
        chapter.paragraphs = paras
