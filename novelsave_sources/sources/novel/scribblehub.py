import datetime
from typing import List
from urllib.parse import quote_plus

from bs4 import BeautifulSoup

from .source import Source
from ...models import Chapter, Metadata, Novel


class ScribbleHub(Source):
    name = "Scribble Hub"
    base_urls = ("https://www.scribblehub.com",)
    last_updated = datetime.date(2021, 10, 29)
    search_viable = True

    search_url_template = "https://www.scribblehub.com/?s={}&post_type=fictionposts"

    def search(self, keyword: str, *args, **kwargs) -> List[Novel]:
        search_url = self.search_url_template.format(quote_plus(keyword))
        soup = self.get_soup(search_url)

        novels = []
        for div in soup.select("div.search_main_box"):
            a = div.select_one(".search_title a")

            novel = Novel(
                title=a.text.strip(),
                url=self.to_absolute_url(a["href"]),
                thumbnail_url=div.select_one(".search_img img").get("src"),
            )

            novels.append(novel)

        return novels

    def novel(self, url: str) -> Novel:
        soup = self.get_soup(url)

        novel = Novel(
            title=soup.select_one("div.fic_title").text.strip(),
            author=soup.select_one("span.auth_name_fic").text.strip(),
            synopsis=[p.text.strip() for p in soup.select(".wi_fic_desc > p")],
            thumbnail_url=soup.select_one(".fic_image img")["src"],
            url=url,
        )

        for a in soup.select("a.fic_genre"):
            novel.metadata.append(Metadata("subject", a.text.strip()))

        for a in soup.select("a.stag"):
            novel.metadata.append(Metadata("tag", a.text.strip()))

        id_ = int(url.split("/")[4])

        volume = novel.get_default_volume()
        volume.chapters = self.parse_toc(id_)

        return novel

    def chapter(self, chapter: Chapter):
        soup = self.get_soup(chapter.url)

        chapter.title = soup.select_one(".chapter-title").text.strip()
        chapter.paragraphs = str(soup.select_one("#chp_raw"))

    def parse_toc(self, id_: int) -> List[Chapter]:
        response = self.http_gateway.post(
            "https://www.scribblehub.com/wp-admin/admin-ajax.php",
            data={
                "action": "wi_getreleases_pagination",
                "pagenum": -1,
                "mypostid": id_,
            },
        )

        soup = BeautifulSoup(response.content, "lxml")

        chapters = []
        for i, li in enumerate(reversed(soup.select("li.toc_w"))):
            a = li.select_one("a")

            chapter = Chapter(
                index=i,
                title=a.text.strip(),
                url=a["href"],
                updated=datetime.datetime.strptime(
                    li.select_one(".fic_date_pub").get("title"), "%b %d, %Y %I:%M %p"
                ),
            )

            chapters.append(chapter)

        return chapters
