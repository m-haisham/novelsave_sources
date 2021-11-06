from novelsave_sources import Metadata, Novel, Volume


def test_get_default_volume_inital_empty():
    novel = Novel("", "")
    assert len(novel.volumes) == 0

    volume = novel.get_default_volume()
    assert isinstance(volume, Volume)

    assert len(novel.volumes) == 1
    assert [volume] == novel.volumes


def test_get_default_volume_with_volume():
    novel = Novel("", "")
    volume = Volume(0, "")

    novel.volumes = [volume]
    assert len(novel.volumes) == 1

    retrieved_volume = novel.get_default_volume()
    assert retrieved_volume == volume


def test_add_metadata():
    novel = Novel("", "")
    novel.add_metadata("name", "value", {"role": "none"})

    assert len(novel.metadata) == 1
    assert novel.metadata[0] == Metadata("name", "value", {"role": "none"})
