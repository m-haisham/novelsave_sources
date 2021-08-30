from dataclasses import dataclass, field
from typing import Optional


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
    others: dict = field(default_factory=lambda: {})
    namespace: Optional[str] = DUBLIN_CORE

    @classmethod
    def custom(cls, name: str, value: str, others: dict = None):
        return cls(name, value, others or {}, cls.CUSTOM)
