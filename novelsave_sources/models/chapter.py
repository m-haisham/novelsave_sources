from dataclasses import dataclass


@dataclass
class Chapter:
    index: int = -1
    no: float = None
    title: str = None
    paragraphs: str = None
    url: str = None

