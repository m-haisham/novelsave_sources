from novelsave_sources import Novel, Volume


def test_get_default_volume_inital_empty():
    novel = Novel('', '')
    assert len(novel.volumes) == 0

    volume = novel.get_default_volume()
    assert isinstance(volume, Volume)

    assert len(novel.volumes) == 1
    assert [volume] == novel.volumes


def test_get_default_volume_with_volume():
    novel = Novel('', '')
    volume = Volume(0, '')

    novel.volumes = [volume]
    assert len(novel.volumes) == 1

    retrieved_volume = novel.get_default_volume()
    assert retrieved_volume == volume

