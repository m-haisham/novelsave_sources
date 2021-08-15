import unittest

from novelsave_sources.models import Chapter
from novelsave_sources.sources.novel.rainofsnow import RainOfSnow


class TestRainOfSnow(unittest.TestCase):

    test_novel_url = 'https://rainofsnow.com/mr-dior/#chapter'
    test_chapter_url = 'https://rainofsnow.com/chapters/mr-dior-ch-25/?novelid=143'

    source = RainOfSnow()

    def test_novel(self):
        novel, chapters, metadata = self.source.novel(self.test_novel_url)
        for key in ('title', 'author', 'url'):
            self.assertIsNotNone(getattr(novel, key))

        self.assertNotEqual(0, len(chapters))
        self.assertIsInstance(metadata, (list, ))

    def test_chapter(self):
        chapter = Chapter(url=self.test_chapter_url)
        self.source.chapter(chapter)

        self.assertIsNotNone(chapter.paragraphs)
