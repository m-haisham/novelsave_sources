from novelsave_sources import Chapter, Volume


def test_static_default():
    assert isinstance(Volume.default(), Volume)


def test_add():
    volume = Volume(-1, "")
    assert len(volume.chapters) == 0

    chapter = Chapter()
    volume.add(chapter)

    assert len(volume.chapters) == 1
    assert volume.chapters[0] == chapter
