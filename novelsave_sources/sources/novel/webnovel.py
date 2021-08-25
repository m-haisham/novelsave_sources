import json
from typing import Tuple, List, Dict, Optional

from bs4 import BeautifulSoup

from .source import Source
from ...exceptions import BadResponseException
from ...models import Novel, Chapter, Metadata
from ...utils.cookies import BlockAll

book_info_url = 'https://www.webnovel.com/book/%s'
chapter_info_url = ''


class Webnovel(Source):
    name = 'Webnovel'
    base_urls = ('https://www.webnovel.com',)

    csrf: str = None

    def __init__(self):
        super(Webnovel, self).__init__()

    def get_csrf(self):
        if not self.csrf:
            self.session.get(self.base_urls[0])
            self.csrf = self.session.cookies.get('_csrfToken')

    def novel(self, url: str) -> Tuple[Novel, List[Chapter], List[Metadata]]:
        soup = self.soup(url)
        novel_id = self.parse_novel_url(url)
        self.csrf = self.session.cookies.get('_csrfToken')

        chapter_list_url = f'https://www.webnovel.com/apiajax/chapter/GetChapterList?_csrfToken={self.csrf}&bookId={novel_id}'
        data = self.validate(self.request_get(chapter_list_url))['data']

        synopsis = '\n'.join([
            para
            for para in soup.select_one("div[class*='j_synopsis'] > p").find_all(text=True, recursive=False)
            if para.strip()
        ])

        novel = Novel(
            title=data['bookInfo']['bookName'],
            synopsis=synopsis,
            thumbnail_url=f'https://img.webnovel.com/bookcover/{novel_id}',
            url=url,
        )

        metadata = []
        writer_elements = soup.select('._mn > address > p > *')
        for i in range(len(writer_elements) // 2):
            label = writer_elements[i * 2].text.strip(': ').lower()
            value = writer_elements[i * 2 + 1].text

            if label == 'author':
                novel.author = value
            else:
                metadata.append(Metadata('author', value, others={'role': label}))

        for a in soup.select('.m-tags a'):
            metadata.append(Metadata('subject', a['title']))

        return novel, self.toc(novel_id, data), metadata

    def chapter(self, chapter: Chapter):
        self.get_csrf()
        novel_id, chapter_id = self.parse_chapter_url(chapter.url)
        response = self.session.get(
            'https://www.webnovel.com/go/pcm/chapter/getContent',
            params={
                '_csrfToken': self.session.cookies.get('_csrfToken', ''),
                'bookId': novel_id,
                'chapterId': chapter_id
            }
        )

        response = self.validate(response)
        data = response['data']['chapterInfo']

        content = BeautifulSoup(
            '<div><p>' + '</p><p>'.join([para['content'] for para in data['contents']]) + '</p></div>', 'lxml')
        self.clean_contents(content)

        chapter.title = data['chapterName']
        chapter.paragraphs = str(content.select_one('div'))

    def toc(self, novel_id, data: dict) -> List[Chapter]:
        chapters = []
        if 'volumeItems' in data:
            for volume in data['volumeItems']:
                chapters += self.make_chapters_from_json(novel_id, volume['chapterItems'], volume)
        elif 'chapterItems' in data:
            chapters += self.make_chapters_from_json(novel_id, data['chapterItems'], None)

        return chapters

    def make_chapters_from_json(self, novel_id, chapter_items, volume: Optional[dict]):
        chapters = []

        if volume:
            volume = (volume['index'], volume['name'])

        for chapter_json in chapter_items:
            if not chapter_json['isAuth']:
                continue

            chapter = Chapter(
                index=chapter_json['index'],
                title=chapter_json['name'],
                volume=volume,
                url=f'https://www.webnovel.com/book/{novel_id}/{chapter_json["id"]}',
            )

            chapters.append(chapter)

        return chapters

    @staticmethod
    def validate(response) -> Dict:
        parsed = json.loads(response.content)
        try:
            # code 0 denotes a successful response
            if parsed['code'] != 0:
                raise BadResponseException(parsed['msg'])

        # for instances it doesnt return any data
        except KeyError:
            raise BadResponseException('no data was returned')

        return parsed

    @staticmethod
    def parse_novel_url(novel_url):
        """
        :return: url of novel
        """
        try:
            return int(novel_url.split('/')[4])
        except ValueError:
            return int(novel_url.split('_')[-1])

    @staticmethod
    def parse_chapter_url(chapter_url) -> Tuple[int, int]:
        """
        :return: novel_id, chapter_id
        """
        pieces = chapter_url.split('/')
        try:
            return int(pieces[4]), int(pieces[5])
        except ValueError:
            return int(pieces[4].split('_')[-1]), int(pieces[5].split('_')[-1])
