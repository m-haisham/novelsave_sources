from dataclasses import dataclass, field
from typing import List


@dataclass
class Novel:
    title: str = None
    author: str = '<Not specified>'
    synopsis: str = None
    thumbnail_url: str = None
    lang: str = 'en'
    url: str = None

    meta_source: str = None
    meta: List[dict] = field(default_factory=lambda: [])

    def add_meta(self, name: str, value: str, namespace: str = 'DC', others=None):
        self.meta.append({
            'namespace': namespace,
            'name': name,
            'value': value,
            'others': others or {},
        })
