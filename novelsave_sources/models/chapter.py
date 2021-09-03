from dataclasses import dataclass


@dataclass
class Chapter:
    index: int = -1
    no: float = None
    title: str = None
    paragraphs: str = None
    url: str = None

    def __hash__(self):
        return hash(self.url)

    def __eq__(self, other):
        return self.url == other.url
