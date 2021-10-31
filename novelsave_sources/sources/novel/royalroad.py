import datetime
from typing import List
from urllib.parse import quote_plus

from .source import Source
from ...models import Chapter, Metadata, Novel


class RoyalRoad(Source):
    name = "Royal Road"
    base_urls = ("https://www.royalroad.com",)
    last_updated = datetime.date(2021, 10, 29)
    search_viable = True

    search_url_template = "https://www.royalroad.com/fictions/search?title={0}&page={1}"

    def search(self, keyword: str, *args, **kwargs) -> List[Novel]:
        search_url = self.search_url_template.format(quote_plus(keyword), 1)
        soup = self.get_soup(search_url)

        novels = []
        for div in soup.select(".fiction-list-item"):
            a = soup.select_one(".fiction-title a")

            novel = Novel(
                title=a.text.strip(),
                url=self.to_absolute_url(a.get("href")),
                thumbnail_url=self.to_absolute_url(div.select_one("img").get("src")),
            )

            for a in div.select(".tags a"):
                novel.add_metadata("subject", a.text.strip())

            novels.append(novel)

        return novels

    def novel(self, url: str) -> Novel:
        soup = self.get_soup(url)

        novel = Novel(
            title=soup.select_one('h1[property="name"]').text.strip(),
            author=soup.select_one('span[property="name"]').text.strip(),
            thumbnail_url=soup.select_one(".page-content-inner .thumbnail")["src"],
            synopsis=[
                p.text.strip()
                for p in soup.select('.description > [property="description"] > p')
            ],
            url=url,
        )

        for a in soup.select('a.label[href*="tag"]'):
            novel.metadata.append(Metadata("subject", a.text.strip()))

        volume = novel.get_default_volume()
        for tr in soup.select("tbody > tr"):
            a = tr.select_one("a[href]")

            chapter = Chapter(
                index=len(volume.chapters),
                title=a.text.strip(),
                url=self.base_urls[0] + a["href"],
                updated=datetime.datetime.strptime(
                    tr.select_one("time").get("title"), "%A, %B %d, %Y %I:%M %p"
                ),
            )

            volume.chapters.append(chapter)

        return novel

    def chapter(self, chapter: Chapter):
        soup = self.get_soup(chapter.url)

        contents = soup.select_one(".chapter-content")
        self.clean_contents(contents)

        chapter.title = soup.find("h1").text.strip()
        chapter.paragraphs = str(contents)
