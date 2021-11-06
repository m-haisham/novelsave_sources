import datetime
from urllib.parse import parse_qs, urlparse

from novelsave_sources import Chapter, Metadata, Novel
from .source import Source


class FirstKissNovel(Source):
    name = "1stKissNovel"
    base_urls = ("https://1stkissnovel.love",)
    last_updated = datetime.date(2021, 10, 14)

    def novel(self, url: str) -> Novel:
        soup = self.get_soup(url.replace("https:", "http:"))

        possible_title = soup.select_one(".post-title h1")
        for span in possible_title.select("span"):
            span.extract()

        author = " ".join(
            a.text.strip()
            for a in soup.select('.author-content a[href*="manga-author"]')
        )

        novel = Novel(
            title=possible_title.text.strip(),
            author=author,
            thumbnail_url=self.to_absolute_url(
                soup.select_one(".summary_image a img")["src"], current_url=url
            ),
            synopsis=soup.select_one(".summary__content").text.strip().splitlines(),
            url=url,
        )

        for a in soup.select(".genres-content > a"):
            novel.metadata.append(Metadata("subject", a.text.strip()))

        shortlink = soup.select_one('link[rel="shortlink"]')["href"]
        novel_id = parse_qs(urlparse(shortlink).query)["p"][0]

        response = self.http_gateway.post(
            "https://1stkissnovel.love/wp-admin/admin-ajax.php",
            data={
                "action": "manga_get_chapters",
                "manga": novel_id,
            },
        )

        soup = self.make_soup(response.content)
        volume = novel.get_default_volume()
        for a in reversed(soup.select(".wp-manga-chapter a")):
            chapter = Chapter(
                index=len(volume.chapters),
                title=a.text.strip(),
                url=self.to_absolute_url(a["href"], current_url=url),
            )

            volume.chapters.append(chapter)

        return novel

    def chapter(self, chapter: Chapter):
        soup = self.get_soup(chapter.url)

        contents = soup.select_one("div.text-left")
        for bad in contents.select("h3, .code-block, script, .adsbygoogle"):
            bad.extract()

        self.clean_contents(contents)

        chapter.paragraphs = str(contents)
