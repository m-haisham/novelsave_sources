from urllib.parse import urlparse


class UrlMixin:
    """A mixin class that provides useful url utility functionality"""

    def clean_url(self, url: str) -> str:
        """Remove query and other addons from url"""
        pr = urlparse(url)
        return f'{pr.scheme}://{pr.netloc}{pr.path}'
