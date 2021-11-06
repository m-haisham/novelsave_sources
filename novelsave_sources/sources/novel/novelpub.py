import datetime
import html
from typing import List
from urllib.parse import quote_plus

from .source import Source
from ...models import Chapter, Novel


class NovelPub(Source):
    base_urls = ("https://www.novelpub.com",)
    last_updated = datetime.date(2021, 10, 29)
    search_viable = True

    search_url_template = "https://www.novelpub.com/lnwsearchlive?inputContent={}"

    def __init__(self, *args, **kwargs):
        super(NovelPub, self).__init__(*args, **kwargs)
        self.bad_tags += ["i"]

    def search(self, keyword: str, *args, **kwargs) -> List[Novel]:
        search_url = self.search_url_template.format(quote_plus(keyword))
        response = self.http_gateway.get(search_url)
        html_content = html.unescape(response.json().get("resultview"))
        soup = self.make_soup(html_content)

        novels = []
        for a in soup.select(".novel-list .novel-item > a"):
            novel = Novel(
                title=a["title"].strip(),
                url=self.to_absolute_url(a["href"]),
                thumbnail_url=a.select_one("img")["src"],
            )

            novels.append(novel)

        return novels

    def novel(self, url: str) -> Novel:
        soup = self.get_soup(url)

        novel = Novel(
            title=soup.select_one(".novel-title").text.strip(),
            author=soup.select_one(".author a").text.strip(),
            synopsis=[
                p.text.strip()
                for p in soup.select(".summary .content p")
                if p.text.strip()
            ],
            thumbnail_url=soup.select_one(".cover img")["data-src"],
            url=url,
        )

        alternative_title = soup.select_one(".alternative-title")
        if alternative_title and alternative_title.text.strip():
            novel.add_metadata(
                "title", alternative_title.text.strip(), others={"role": "alt"}
            )

        for li in soup.select(".categories > ul > li"):
            novel.add_metadata("subject", li.text.strip())

        for a in soup.select(".content .tag"):
            novel.add_metadata("tag", a.text.strip())

        for span in soup.select(".header-stats span"):
            label = span.select_one("small").text.strip().lower()
            if label == "status":
                value = span.select_one("strong").text.strip()
                novel.status = value

        volume = novel.get_default_volume()

        toc_url = url.rstrip("/") + "/chapters/page-{}"
        soup = self.get_soup(toc_url.format(1))
        self.extract_toc(soup, volume)

        pages = soup.select(".pagenav .pagination > li:not(.PagedList-skipToNext)")
        pages = (
            range(
                2, int(pages[-1].select_one("a")["href"].rsplit("-", 1)[-1].strip()) + 1
            )
            if len(pages) > 1
            else range(0, 0)
        )
        for page in pages:
            self.extract_toc(self.get_soup(toc_url.format(page)), volume)

        return novel

    def extract_toc(self, soup, volume):
        for li in soup.select(".chapter-list > li"):
            a = li.select_one("a")

            updated = li.select_one("time").get("datetime", None)

            chapter = Chapter(
                index=int(li["data-orderno"]),
                title=a.select_one(".chapter-title").text.strip(),
                url=self.to_absolute_url(a["href"]),
                updated=datetime.datetime.fromisoformat(updated) if updated else None,
            )

            volume.add(chapter)

    def chapter(self, chapter: Chapter):
        soup = self.get_soup(chapter.url)
        content = soup.select_one("#chapter-container")
        for element in content.select(".adsbox, adsbygoogle"):
            element.extract()

        self.clean_contents(content)

        chapter.paragraphs = str(content)
