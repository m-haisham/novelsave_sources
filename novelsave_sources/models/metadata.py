from dataclasses import dataclass

DUBLIN_CORE_TAGS = [
    'title', 'language', 'subject',
    'creator', 'contributor', 'publisher', 'rights',
    'coverage', 'date', 'description',
]


@dataclass
class Metadata:
    """
    'DC' also known as Dublin Core metadata contains the following:

    Minimal required:

    - DC:identifier
    - DC:title
    - DC:language

    Optional:

    - DC:creator
    - DC:contributor
    - DC:publisher
    - DC:rights
    - DC:coverage
    - DC:date
    - DC:description
    """

    DUBLIN_CORE = 'DC'
    CUSTOM = 'OPF'

    name: str
    value: str
    others: dict
    namespace: str

    def __init__(self, name: str, value: str, others: dict = None):
        self.name = name
        self.value = value
        self.others = others or {}
        self.namespace = self.DUBLIN_CORE if name in DUBLIN_CORE_TAGS else self.CUSTOM
