import datetime
import re
from time import time
from urllib.parse import urlparse

from .source import Source
from ...models import Chapter, Novel, Metadata

chapter_info_url = 'https://www.wattpad.com/v4/parts/{id}?fields=id,title,pages,text_url&_={key}'
story_info_url = 'https://www.wattpad.com/api/v3/stories/{id}'


class WattPad(Source):
    name = 'Wattpad'
    base_urls = ('https://www.wattpad.com', 'https://my.w.tt',)
    last_updated = datetime.date(2021, 9, 6)

    def __init__(self):
        super(WattPad, self).__init__()
        self.decimal = re.compile(r'\d+')

    def novel(self, url: str) -> Novel:
        info_url = story_info_url.format(id=self.decimal.search(url).group())
        data = self.request_get(info_url).json()

        novel = Novel(
            title=data['title'],
            thumbnail_url=data['cover'],
            author=data['user']['name'],
            synopsis=[t.strip() for t in data['description'].split('\n') if t.strip()],
            url=url,
        )

        for tag in data['tags']:
            novel.metadata.append(Metadata('tag', tag))

        novel.metadata.append(Metadata('status', 'Completed' if data['completed'] else 'Ongoing'))
        novel.metadata.append(Metadata('date', data['createDate']))

        volume = novel.get_default_volume()
        for part in data['parts']:
            chapter = Chapter(
                index=len(volume.chapters),
                title=part['title'],
                url=part['url'],
            )

            volume.chapters.append(chapter)

        return novel

    def chapter(self, chapter: Chapter):
        chapter_id = urlparse(chapter.url).path.split('-', maxsplit=1)[0].strip('/')
        info_url = chapter_info_url.format(id=chapter_id, key=int(time() * 1000))
        data = self.request_get(info_url).json()

        text = self.request_get(data['text_url']['text']).content.decode('utf-8')
        text = re.sub(r'<p data-p-id="[a-f0-9]+">', '<p>', text)

        chapter.title = data['title']
        chapter.paragraphs = text
