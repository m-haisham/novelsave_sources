import re
from abc import abstractmethod
from urllib.parse import urlparse

from .source import Source
from ...models import Novel, Chapter


class WordPress(Source):
    def novel(self, url: str) -> Novel:
        soup = self.get_soup(url)

        novel = Novel(
            title=soup.select_one('meta[property="og:title"]')["content"],
            author=soup.select_one('meta[property="og:site_name"]')["content"],
            thumbnail_url=soup.select_one('meta[property="og:image"]')["content"],
            url=url,
            lang=self.lang,
        )

        # Removes none TOC links from bottom of page.
        toc_parts = soup.select_one("div.entry-content")
        for notoc in toc_parts.select(
            ".sharedaddy, .inline-ad-slot, .code-block, script, hr, .adsbygoogle"
        ):
            notoc.extract()

        volume = novel.get_default_volume()
        hostname = urlparse(url).hostname or ""
        for a in soup.select("div.entry-content a"):

            # check for external links
            if not re.search(hostname + r"/\d{4}/\d{2}/", a["href"]):
                continue

            volume.add(
                Chapter(
                    index=len(volume.chapters),
                    title=a.text.strip(),
                    url=self.to_absolute_url(a["href"]),
                )
            )

        return novel

    def chapter(self, chapter: Chapter):
        soup = self.get_soup(chapter.url)

        body_parts = soup.select_one("div.entry-content")

        chapter.paragraphs = self.parse_content(body_parts)

    @abstractmethod
    def parse_content(self, element) -> str:
        """Parse the element and return the string"""
