from urllib.parse import urlparse

from deprecation import deprecated

from .. import __version__


@deprecated(deprecated_in='0.3.1', removed_in='0.4.0', current_version=__version__,
            details='Use <novelsave_sources.utils.mixins.UrlMixin.clean_url> instead')
def clean_url(url: str) -> str:
    """Remove query and other addons from url"""
    pr = urlparse(url)
    return f'{pr.scheme}://{pr.netloc}{pr.path}'
