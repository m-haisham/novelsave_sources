import pytest

from novelsave_sources.utils.mixins import UrlMixin


@pytest.fixture
def url_mixin():
    return UrlMixin()


@pytest.mark.parametrize('url, expected_result', [
    ('https://website.com/#tab-chapters-title', 'https://website.com/'),
    ('http://website.net/#place?query', 'http://website.net/'),
    ('http://website.net#place?query', 'http://website.net'),
])
def test_clean_url(url_mixin, url, expected_result):
    assert url_mixin.clean_url(url) == expected_result
