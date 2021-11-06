import pytest

from novelsave_sources.utils import helpers


@pytest.mark.parametrize(
    "url, expected_result",
    [
        ("https://website.com/#tab-chapters-title", "https://website.com/"),
        ("http://website.net/#place?query", "http://website.net/"),
        ("http://website.net#place?query", "http://website.net"),
    ],
)
def test_clean_url(url, expected_result):
    assert helpers.clean_url(url) == expected_result
