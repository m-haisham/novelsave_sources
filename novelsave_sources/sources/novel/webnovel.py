import json
from typing import Tuple, List, Dict

from .source import Source
from ...exceptions import BadResponseException
from ...models import Novel, Chapter, Metadata
from ...utils.cookies import BlockAll


class Webnovel(Source):
    name = 'Webnovel'
    base_urls = ('https://www.webnovel.com',)

    def __init__(self):
        super(Webnovel, self).__init__()
        self.session.cookies.set_policy(BlockAll())

    def novel(self, url: str) -> Tuple[Novel, List[Chapter], List[Metadata]]:
        soup = self.soup(url)
        metadata = []
        novel_id = self.parse_novel_url(url)

        info_elements = soup.select('._mn > *')
        writer_elements = info_elements[2].select('p > *')

        novel = Novel(
            title=info_elements[0].text[:-len(info_elements[0].find('small').text) - 1][0],
            synopsis=soup.select_one("div[class*='j_synopsis'] > p").text,
            thumbnail_url=f'https://img.webnovel.com/bookcover/{novel_id}',
            url=url,
        )

        # writer info
        for i in range(round(len(writer_elements) / 2)):
            label = writer_elements[i * 2].text.strip(': ').lower()
            value = writer_elements[i * 2 + 1].text

            if label == 'author':
                novel.author = value
            else:
                metadata.append(Metadata('author', value, others={'role': label}))

        return novel, self.toc(novel_id), metadata

    def chapter(self, chapter: Chapter):
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

        chapter.title = data['chapterName']
        chapter.paragraphs = '<p>' + '</p><p>'.join([para['content'] for para in data['contents']]) + '</p>'

    def toc(self, novel_id: int) -> List[Chapter]:
        response = self.session.get(
            'https://www.webnovel.com/apiajax/chapter/GetChapterList',
            params={
                '_csrfToken': self.session.cookies.get('_csrfToken'),
                'bookId': novel_id,
            }
        )

        response_json = self.validate(response)
        volumes = response_json['data']['volumeItems']

        chapters = []
        for volume_index, volume in enumerate(volumes):

            for chapter_json in volume['chapterItems']:
                if int(chapter_json['isAuth']):
                    Chapter(
                        index=chapter_json['index'],
                        title=chapter_json['name'],
                        volume=(volume['index'], volume['name']),
                        url=f'https://www.webnovel.com/book/{novel_id}/{chapter_json["id"]}',
                    )

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
