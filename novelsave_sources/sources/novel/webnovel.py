import datetime
import json
from typing import Tuple, List, Dict, Optional

from bs4 import BeautifulSoup

from .source import Source
from ...exceptions import BadResponseException
from ...models import Novel, Chapter, Metadata

book_info_url = 'https://www.webnovel.com/book/%s'
chapter_list_url = 'https://www.webnovel.com/go/pcm/chapter/get-chapter-list?_csrfToken={csrf}&bookId={id}&pageIndex=0'


class Webnovel(Source):
    name = 'Webnovel'
    base_urls = ('https://www.webnovel.com',)
    last_updated = datetime.date(2021, 9, 3)

    csrf_token: str = None

    def __init__(self):
        super(Webnovel, self).__init__()

    def get_csrf(self):
        if not self.csrf_token:
            self.session.get(self.base_urls[0])
            self.csrf_token = self.session.cookies.get('_csrfToken')

    def novel(self, url: str) -> Tuple[Novel, List[Chapter], List[Metadata]]:
        soup = self.get_soup(url)
        novel_id = self.parse_novel_url(url)
        self.csrf_token = self.session.cookies.get('_csrfToken')

        data = self.validate(self.request_get(chapter_list_url.format(csrf=self.csrf_token, id=novel_id)))['data']

        synopsis = '\n'.join([
            para
            for para in soup.select_one("div[class*='j_synopsis'] > p").find_all(text=True, recursive=False)
            if para.strip()
        ])

        novel = Novel(
            title=data['bookInfo']['bookName'],
            synopsis=synopsis,
            thumbnail_url=f'https://img.webnovel.com/bookcover/{novel_id}',
            url=f'https://www.webnovel.com/book/{novel_id}',
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

    def make_chapters_from_json(self, novel_id, chapter_items, volume_data: Optional[dict]):
        chapters = []

        volume = None
        if volume_data:
            volume = (volume_data['volumeId'], volume_data['volumeName'])

        for chapter_data in chapter_items:
            if not chapter_data['isAuth']:
                continue

            chapter = Chapter(
                index=chapter_data['chapterIndex'],
                title=f'{chapter_data["chapterIndex"]} {chapter_data["chapterName"]}',
                volume=volume,
                url=f'https://www.webnovel.com/book/{novel_id}/{chapter_data["chapterId"]}',
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
        novel_url = novel_url.rstrip('/')
        try:
            return int(novel_url.split('/')[4])
        except ValueError:
            return int(novel_url.split('_')[-1])

    @staticmethod
    def parse_chapter_url(chapter_url) -> Tuple[int, int]:
        """
        :return: novel_id, chapter_id
        """
        pieces = chapter_url.rstrip('/').split('/')
        try:
            return int(pieces[4]), int(pieces[5])
        except ValueError:
            return int(pieces[4].split('_')[-1]), int(pieces[5].split('_')[-1])
