from dataclasses import dataclass
from typing import Optional


@dataclass
class Novel:
    title: str = None
    author: Optional[str] = None
    synopsis: str = None
    thumbnail_url: str = None
    lang: str = 'en'
    url: str = None
