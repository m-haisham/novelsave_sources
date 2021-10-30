from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Chapter:
    index: int = -1
    title: str = None
    paragraphs: str = None
    url: str = None
    updated: Optional[datetime] = None
