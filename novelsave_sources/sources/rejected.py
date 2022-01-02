import datetime
from collections import namedtuple

Rejected = namedtuple("Rejected", "lang base_url reason added")

rejected_sources = [
    Rejected(
        lang="multi",
        base_url="https://www.fanfiction.net",
        reason="Has cloudflare bot protection",
        added=datetime.date(2021, 10, 30),
    ),
    Rejected(
        lang="en",
        base_url="https://mtlnation.com",
        reason="Has cloudflare bot protection",
        added=datetime.date(2022, 1, 2),
    ),
]
