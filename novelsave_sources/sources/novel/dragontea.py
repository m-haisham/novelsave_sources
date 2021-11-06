import datetime
from functools import lru_cache
from typing import Dict

from .source import Source
from ...models import Chapter, Metadata, Novel


class DragonTea(Source):
    name = "Dragon Tea"
    base_urls = ("https://dragontea.ink/",)
    last_updated = datetime.date(2021, 10, 7)

    def __init__(self, *args, **kwargs):
        super(DragonTea, self).__init__(*args, **kwargs)
        self.bad_tags += ["h1", "h2", "h3", "h4", "h5", "h6", "hr"]

    def novel(self, url: str) -> Novel:
        http_url = url.replace("https:", "http:")
        soup = self.get_soup(http_url)

        jumble_map = self.jumble_map()

        novel = Novel(
            title=soup.select_one(".post-title").text.strip(),
            author=soup.select_one(".author-content").text.strip(),
            thumbnail_url=self.to_absolute_url(
                soup.select_one(".summary_image img")["src"], url
            ),
            synopsis=[
                self.reorder_text(jumble_map, p).text.strip()
                for p in soup.select(".summary__content > p")
            ],
            url=url,
        )

        # other metadata
        for item in soup.select(".post-content_item"):
            key = item.select_one(".summary-heading").text.strip()
            value = item.select_one(".summary-content").text.strip()
            if key == "Alternative":
                novel.metadata.append(Metadata("title", value, others={"role": "alt"}))
            elif key == "Type":
                novel.metadata.append(Metadata("type", value))

        for a in soup.select(".genres-content > a"):
            novel.metadata.append(Metadata("subject", a.text.strip()))

        for a in soup.select(".tags-content > a"):
            novel.metadata.append(Metadata("tag", a.text.strip()))

        artist_content = soup.select_one(".artist-content > a")
        if artist_content:
            novel.metadata.append(
                Metadata(
                    "contributor", artist_content.text.strip(), others={"role": "ill"}
                )
            )

        soup = self.get_soup(http_url.rstrip("/") + "/ajax/chapters/", method="POST")
        volume = novel.get_default_volume()
        for a in reversed(soup.select(".wp-manga-chapter > a")):
            chapter = Chapter(
                index=len(volume.chapters),
                title=a.text.strip(),
                url=self.to_absolute_url(a["href"]),
            )

            volume.chapters.append(chapter)

        return novel

    def chapter(self, chapter: Chapter):
        soup = self.get_soup(chapter.url.replace("https:", "http:"))

        # text-left has a better collection of paragraphs...
        # however we are not taking any chances assuming its always there
        content = soup.select_one(".text-left, .reading-content")

        self.clean_contents(content)

        jumble_map = self.jumble_map()
        for p in content.select("p"):
            if not p.text.strip():
                p.extract()
                continue

            self.reorder_text(jumble_map, p)

        chapter.title = soup.select_one(".breadcrumb > li.active").text.strip()
        chapter.paragraphs = str(content)

    normal_char_set = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    jumble_char_set = "ZYXWVUTSRQPONMLKJIHGFEDCBAzyxwvutsrqponmlkjihgfedcba"

    @lru_cache(1)
    def jumble_map(self) -> Dict[str, str]:
        return {jc: nc for jc, nc in zip(self.jumble_char_set, self.normal_char_set)}

    @staticmethod
    def reorder_text(jumble_map, element):
        text = ""
        for char in element.text:
            try:
                text += jumble_map[char]
            except KeyError:
                text += char

        element.string = text

        return element
