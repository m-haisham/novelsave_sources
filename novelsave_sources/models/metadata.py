from dataclasses import dataclass

DUBLIN_CORE_TAGS = [
    "title",
    "language",
    "subject",
    "creator",
    "contributor",
    "publisher",
    "rights",
    "coverage",
    "date",
    "description",
]


@dataclass
class Metadata:
    """Data class that holds a single value of metadata for novels

    Attributes:
        name (str): Name of the metadata

            Example: ``subject``, ``tag``

        value (str): Value of the metadata

        others (dict): A dictionary value defining other attributes of the metadata

        namespace (str): The namespace of the metadata. This is either Dublin Core (DC)
            or OPF.

            Dublin Core (DC) has the following tags:

                ``title``, ``language``, ``subject``, ``creator``, ``contributor``, ``publisher``,
                ``rights``, ``coverage``, ``date``, ``description``

            The :meth:`__init__` method automatically identifies the namespace.
    """

    DUBLIN_CORE = "DC"
    CUSTOM = "OPF"

    name: str
    value: str
    others: dict
    namespace: str

    def __init__(self, name: str, value: str, others: dict = None):
        """
        The namespace attribute is calculated by checking if the :attr:`name`
        exists in dublin core tags. If so, namespace is set Dublin Core (DC)
        otherwise it is set OPF.

        Refer to :attr:`name`, :attr:`value`, and :attr:`others` for more
        details on parameters.
        """
        self.name = name
        self.value = value
        self.others = others or {}
        self.namespace = self.DUBLIN_CORE if name in DUBLIN_CORE_TAGS else self.CUSTOM
