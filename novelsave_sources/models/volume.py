from dataclasses import dataclass, field
from typing import List

from .chapter import Chapter


@dataclass
class Volume:
    """Data class that identifies a single volume in a novel

    Attributes:
        index (int): The order of volume in the novel. Lowest first.

        name (str): The name of the volume.

        chapters (List[Chapter]): The chapters belonging to volume under novel.
    """

    index: int
    name: str

    chapters: List[Chapter] = field(default_factory=lambda: [])

    @staticmethod
    def default():
        """Factory method that returns volume object with
        values identifying it as default.

        This method is used when a particular source does not
        define any volumes for the novel
        """
        return Volume(-1, "_default")

    def add(self, chapter: Chapter):
        """Shorthand method to add chapter into this volume"""
        self.chapters.append(chapter)
