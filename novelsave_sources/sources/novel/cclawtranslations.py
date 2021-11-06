import datetime

from .wordpress import WordPress


class CclawTranslations(WordPress):
    base_urls = [
        "https://cclawtranslations.home.blog/",
    ]

    last_updated = datetime.date(2021, 11, 3)

    def init(self):
        self.blacklist_patterns += ["CONTENIDO | SIGUIENTE"]

    def parse_content(self, element) -> str:
        self.clean_contents(element)
        for div in element.find_all("div", recursive=False):
            div.extract()

        return str(element)
