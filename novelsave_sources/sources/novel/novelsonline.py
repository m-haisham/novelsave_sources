import datetime

from .source import Source
from ... import Chapter, Novel


class NovelsOnline(Source):
    base_urls = ["https://novelsonline.net"]
    last_updated = datetime.date(2021, 11, 7)

    def novel(self, url: str) -> Novel:
        soup = self.get_soup(url)

        author_link = soup.select_one("a[href*=author]")
        author = author_link.text.strip().title() if author_link else None

        novel = Novel(
            title=soup.select_one(".block-title h1").text.strip(),
            synopsis=[
                p.text.strip()
                for p in soup.select(".novel-detail-body > p")
                if p.text.strip()
            ],
            author=author,
            url=url,
        )

        novel.thumbnail_url = self.to_absolute_url(
            soup.find("img", {"alt": novel.title})["src"]
        )

        for a in soup.select('.novel-details a[href*="category"]'):
            novel.add_metadata("subject", a.text.strip())

        for a in soup.select('.novel-details a[href*="tags"]'):
            novel.add_metadata("tag", a.text.strip())

        for item in soup.select(".novel-details > .novel-detail-item"):
            header = item.select_one(".novel-detail-header")
            if not header:
                continue

            label = header.text.strip().lower()

            def add_metadata(name, others=None):
                text = item.select_one(".novel-detail-body li").text.strip()
                if text:
                    novel.add_metadata(name, text)

            if label == "type":
                add_metadata("type")
            elif label == "language":
                add_metadata("language", others={"role": "original"})
            elif label == "artist(s)":
                for a in item.select(".novel-detail-body a"):
                    novel.add_metadata(
                        "contributor", a.text.strip(), others={"role": "artist"}
                    )
            elif label == "year":
                add_metadata("date")
            elif label == "status":
                novel.status = item.select_one(".novel-detail-body li").text.strip()

        volume = novel.get_default_volume()
        for a in soup.select(".chapters .chapter-chs li a"):
            index = len(volume.chapters)

            chapter = Chapter(
                index=index,
                url=self.to_absolute_url(a["href"]),
                title=a.text.strip() or ("Chapter %d" % index + 1),
            )

            volume.add(chapter)

        return novel

    def chapter(self, chapter: Chapter):
        soup = self.get_soup(chapter.url)

        div = soup.select_one(".chapter-content3")

        bad_selectors = [
            ".trinity-player-iframe-wrapper" ".hidden",
            ".ads-title",
            "script",
            "center",
            "interaction",
            "a[href*=remove-ads]",
            "a[target=_blank]",
            "hr",
            "br",
            "#growfoodsmart",
            ".col-md-6",
        ]
        for hidden in div.select(", ".join(bad_selectors)):
            hidden.extract()

        self.clean_contents(div)

        chapter.paragraphs = str(div)
