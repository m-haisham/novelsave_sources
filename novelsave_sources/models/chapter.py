from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Chapter:
    """Data class that identifies a single chapter in a novel

    Attributes:
        index (int): The order of chapter in the novel. Lowest first.

        title (str): The title of the chapter.

        paragraphs (Optional[str]): The reading content of the chapter in html.

        url (str): The url pointing to the chapter in the web.

        updated (str): The time this chapter was last updated as defined
            by the source.
    """

    index: int = -1
    title: str = None
    paragraphs: Optional[str] = None
    url: str = None
    updated: Optional[datetime] = None
