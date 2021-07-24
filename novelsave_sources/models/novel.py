from dataclasses import dataclass


@dataclass
class Novel:
    title: str = None
    author: str = '<Not specified>'
    synopsis: str = None
    thumbnail_url: str = None
    lang: str = 'en'
    url: str = None
