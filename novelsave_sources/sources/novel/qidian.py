import datetime

from .source import Source
from ...models import Chapter, Novel, Volume


class Qidian(Source):
    base_urls = ("https://book.qidian.com", "https://read.qidian.com")
    last_updated = datetime.date(2021, 10, 29)
    lang = "zh"

    chapter_list_url = (
        "https://book.qidian.com/ajax/book/category?_csrfToken={0}&bookId={1}"
    )
    chapter_details_url = "https://read.qidian.com/chapter/{}"

    def novel(self, url: str) -> Novel:
        soup = self.get_soup(url)

        book_img = soup.select_one("#bookImg")
        thumbnail = self.to_absolute_url(book_img.find("img")["src"])
        thumbnail = "/".join(thumbnail.rsplit("/", 2)[:-1])

        novel = Novel(
            title=soup.select_one(".book-info h1 em").text.strip(),
            author=soup.select_one(".book-info h1 a.writer").text.strip(),
            thumbnail_url=thumbnail,
            synopsis=self.find_paragraphs(soup.select_one(".book-intro")),
            url=url,
            lang=self.lang,
        )

        for a in soup.select(".tag .red"):
            novel.add_metadata("subject", a.text.strip())

        csrf = self.http_gateway.cookies["_csrfToken"]
        book_id = book_img["data-bid"]

        list_url = self.chapter_list_url.format(csrf, book_id)
        json = self.http_gateway.get(list_url).json()

        c_count = 0
        for v_node in json["data"]["vs"]:
            vid = len(novel.volumes) + 1
            volume = Volume(vid, v_node["vN"])
            novel.volumes.append(volume)

            for c_node in v_node["cs"]:
                chapter = Chapter(
                    index=c_count,
                    title=c_node["cN"],
                    url=self.chapter_details_url.format(c_node.get("cU")),
                    updated=datetime.datetime.fromisoformat(c_node["uT"]),
                )

                volume.add(chapter)
                c_count += 1

        return novel

    def chapter(self, chapter: Chapter):
        soup = self.get_soup(chapter.url)

        chapter.title = soup.select_one("h3.j_chapterName").text.strip()
        chapter.paragraphs = soup.select_one("div.j_readContent").extract()
