from dataclasses import dataclass, field
from typing import List, Optional

from .metadata import Metadata
from .volume import Volume


@dataclass
class Novel:
    """Data class for parsed novels

    Attributes:
        title (str): The name of the novel.

        url (str): The url pointing to the webpage of novel.

        author (Optional[str]): The author of the novel.

        synopsis (List[str]): The description of the novel in lines or paragraphs.

        thumbnail_url (Optional[str]): The url pointing to the thumbnail image of the novel

        status (Optional[str]): The status of the novel, can be ongoing, completed, or hiatus

        lang (str): The language of the novel. This is not the original language, however
            the language this novel is currently readable in.

        volumes (List[Volume]): List of volumes of the novel

        metadata (List[Metadata]): List of metadata of the novel
    """

    title: str
    url: str
    author: Optional[str] = None
    synopsis: List[str] = field(default_factory=lambda: [])
    thumbnail_url: Optional[str] = None
    status: Optional[str] = None
    lang: str = "en"

    volumes: List[Volume] = field(default_factory=lambda: [])
    metadata: List[Metadata] = field(default_factory=lambda: [])

    def get_default_volume(self):
        """Get or create the default volume for the novel

        If the novel already has volumes, this method returns the
        first volume, otherwise creates and adds the default volume to novel
        and returns that volume.
        """
        if self.volumes:
            return self.volumes[0]

        volume = Volume.default()
        self.volumes.append(volume)
        return volume

    def add_metadata(self, *args, **kwargs):
        """Shorthand for adding metadata"""
        self.metadata.append(Metadata(*args, **kwargs))
