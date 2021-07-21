from unittest import TestCase

from novelsave_sources.sources.novel import sources


class TestSource(TestCase):

    def test_requirements(self):
        for source in sources:
            self.assertTrue(source.__name__)

