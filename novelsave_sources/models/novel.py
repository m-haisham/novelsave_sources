from dataclasses import dataclass, field
from typing import Optional, List

from .metadata import Metadata
from .volume import Volume


@dataclass
class Novel:
    title: str
    url: str
    author: Optional[str] = None
    synopsis: str = None
    thumbnail_url: str = None
    lang: str = 'en'

    volumes: List[Volume] = field(default_factory=lambda: [])
    metadata: List[Metadata] = field(default_factory=lambda: [])
