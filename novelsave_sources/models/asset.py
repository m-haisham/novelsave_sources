from dataclasses import dataclass
from typing import Optional


@dataclass
class Asset:
    """
    A class used to represent an asset related to a novel

    ...

    Attributes
    ----------
    name : Optional[str]
        A string that represents the name of the asset (optional)
    url : url
        The source location of the asset
    mimetype : str
        A string that represents the type of the asset from the
        standard MIME (https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types/Common_types)
    scope : Optional[str]
        The scope on which the asset is applied. Most commonly specified as a css selector
        applied to a specific node tree.
    """

    name: Optional[str]
    url: str
    mimetype: str
    scope: Optional[str] = None
