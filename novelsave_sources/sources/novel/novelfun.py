import datetime
import re

from .source import Source
from ...models import Novel, Chapter, Metadata

query = """query chapters_NovelRefetchQuery(
    $slug: String!
    $startChapNum: Int
) {...chapters_list_items} fragment chapters_list_items on Query {
    chapterListChunks(
        bookSlug: $slug,
        chunkSize: %d,
        startChapNum: $startChapNum
    ) {
        items {
            title
            chapNum
            url
        }
    }
}
"""


class NovelFun(Source):
    base_urls = ('https://novelfun.net',)
    last_updated = datetime.date(2021, 9, 7)

    graphql = f'{base_urls[0]}/graphql'

    def novel(self, url: str) -> Novel:
        soup = self.get_soup(url)

        novel = Novel(
            title=soup.select_one('h1').text.strip(),
            author=soup.select_one('a[href*="author"]').text.strip(),
            synopsis=[p.text.strip() for p in soup.select('article > div > p')],
            url=url,
        )

        novel.thumbnail_url = soup.select_one(f'img[title="{novel.title}"]')['src']

        for a in soup.select('td a[href*="genre"]'):
            novel.metadata.append(Metadata('subject', a.text.strip()))

        title_slug = url.rstrip('/').split('/')[-1]
        total = int(re.match(r'(\d+)', soup.select_one('h2 ~ div').text).group(1))
        data = {
            'id_': 'chapters_NovelRefetchQuery',
            'query': query % total,
            'variables': {
                'slug': title_slug,
                'startChapNum': 1,
            },
        }
        data = self.session.get(self.graphql, json=data).json()

        novel.get_default_volume().chapters = [
            Chapter(
                index=c['chapNum'],
                title=f'Chapter {c["chapNum"]}: {c["title"]}',
                url=self.base_urls[0]+c['url'],
            )
            for c in data['data']['chapterListChunks'][0]['items']
        ]

        return novel

    def chapter(self, chapter: Chapter):
        soup = self.get_soup(chapter.url)

        content = soup.select_one('h1 ~ div')
        self.clean_contents(content)

        chapter.paragraphs = str(content)
