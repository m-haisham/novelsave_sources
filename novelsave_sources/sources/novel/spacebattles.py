import datetime
import re
from urllib.parse import urlparse

from .source import Source
from ... import BadResponseException
from ...models import Chapter, Novel


class Spacebattles(Source):
    name = 'SpaceBattles'
    base_urls = ('https://forums.spacebattles.com',)
    last_updated = datetime.date(2021, 9, 9)

    def __init__(self):
        super(Spacebattles, self).__init__()
        self.clear_tags = re.compile(r'(</?div>|<br ?/?>)')

    def novel(self, url: str) -> Novel:
        threadmarks_url = url.rstrip('/') + '/threadmarks/'
        soup = self.get_soup(threadmarks_url)

        author_element = soup.select_one('.username')

        # getting writer profile image
        try:
            author_soup = self.get_soup(self.to_absolute_url(author_element['href']))
            avatar = author_soup.select_one('.avatarWrapper > .avatar')
            thumbnail = self.to_absolute_url(avatar['href'])
        except BadResponseException:
            thumbnail = None

        novel = Novel(
            title=soup.select_one('.p-breadcrumbs > li:last-child').text.strip(),
            author=author_element.text,
            thumbnail_url=thumbnail,
            url=url,
        )

        volume = novel.get_default_volume()
        for i, a in enumerate(soup.select('.block-body--threadmarkBody.is-active > div > div > div:first-child a')):
            chapter = Chapter(
                index=i,
                title=a.text,
                url=self.to_absolute_url(a['href'])
            )

            volume.chapters.append(chapter)

        return novel

    def chapter(self, chapter: Chapter):
        parsed_url = urlparse(chapter.url)
        raw_url = f'{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}'

        soup = self.get_soup(raw_url)

        article = soup.select_one(f'.u-anchorTarget#{parsed_url.fragment}').parent
        content = article.select_one('.message-inner .message-userContent .bbWrapper')

        content.smooth()
        content.attrs.clear()

        paragraphs = [t for t in self.clear_tags.sub('', str(content)).splitlines() if t]

        chapter.title = article.select_one('.message-cell--threadmark-header > span').text.strip()
        chapter.paragraphs = '<p>' + '</p><p>'.join(paragraphs) + '</p>'
