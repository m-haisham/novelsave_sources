from unittest import TestCase

from novelsave_sources.models import Novel


class TextNovel(TestCase):

    def test_add_meta(self):
        data = [
            {'name': 'test1', 'value': 'value1', 'namespace': 'namespace1', 'others': {}},
            {'name': 'test1', 'value': 'value1', 'namespace': 'DC', 'others': {}},
        ]

        novel = Novel()
        novel.add_meta(**data[0])
        novel.add_meta(**{key: value for key, value in data[1].items() if key != 'namespace'})

        for i in range(len(data)):
            self.assertDictEqual(data[i], novel.meta[i])
