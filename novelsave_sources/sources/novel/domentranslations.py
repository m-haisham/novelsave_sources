import datetime

from .wordpress import WordPress


class DomenTranslations(WordPress):
    base_urls = [
        "https://domentranslations.wordpress.com/",
    ]

    last_updated = datetime.date(2021, 11, 3)
    lang = "es"

    def init(self):
        self.blacklist_patterns += ["CONTENIDO | SIGUIENTE"]

    def parse_content(self, element) -> str:
        for div in element.select('div[style*="text-align:center"], .sharedaddy'):
            div.extract()

        self.clean_contents(element)

        return str(element)
