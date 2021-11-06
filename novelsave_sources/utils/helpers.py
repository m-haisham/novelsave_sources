from urllib.parse import urlparse


def clean_url(url: str) -> str:
    """Remove query and other addons from url"""
    pr = urlparse(url)
    return f"{pr.scheme}://{pr.netloc}{pr.path}"
