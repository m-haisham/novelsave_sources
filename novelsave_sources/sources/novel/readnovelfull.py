import datetime

from .source import Source
from ...models import Chapter, Metadata, Novel
from ...utils import helpers


class ReadNovelFull(Source):
    base_urls = ("https://readnovelfull.com/",)
    last_updated = datetime.date(2021, 10, 17)

    def novel(self, url: str) -> Novel:
        soup = self.get_soup(url)

        author = []
        for a in soup.select("ul.info.info-meta li")[1].select("a"):
            author.append(a.text.strip())

        novel = Novel(
            title=soup.select_one("h3.title").text.strip(),
            author=", ".join(author),
            synopsis=[p.text.strip() for p in soup.select(".desc-text > p")],
            thumbnail_url=self.to_absolute_url(soup.select_one("div.book img")["src"]),
            url=helpers.clean_url(url),
        )

        for a in soup.select('.info a[href*="genre"]'):
            novel.metadata.append(Metadata("subject", a.text.strip()))

        alternative_titles_element = soup.select("ul.info.info-meta li")[0]
        alternative_titles_element.select_one("h3").extract()

        for text in alternative_titles_element.text.split(","):
            novel.metadata.append(
                Metadata("title", text.strip(), others={"role": "alt"})
            )

        novel_id = soup.select_one("div#rating")["data-novel-id"]
        chapters_url = (
            f"https://readnovelfull.com/ajax/chapter-archive?novelId={novel_id}"
        )
        chapters_soup = self.get_soup(chapters_url)

        chapters = chapters_soup.select("li a")
        for a in chapters:
            for span in a.findAll("span"):
                span.extract()

        volume = novel.get_default_volume()
        for element in chapters:
            chapter = Chapter(
                index=len(volume.chapters),
                title=element["title"] or f"Chapter {len(volume.chapters)}",
                url=self.to_absolute_url(element["href"]),
            )

            volume.chapters.append(chapter)

        return novel

    def chapter(self, chapter: Chapter):
        soup = self.get_soup(chapter.url)
        content = soup.select_one("#chr-content")
        self.clean_contents(content)

        chapter.paragraphs = str(content)
