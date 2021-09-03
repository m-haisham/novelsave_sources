from dataclasses import dataclass, field
from typing import List

from .chapter import Chapter


@dataclass
class Volume:
    index: int
    name: str

    chapters: List[Chapter] = field(default_factory=lambda: [])

    @staticmethod
    def default():
        return Volume(-1, '_default')
