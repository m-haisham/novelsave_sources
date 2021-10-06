import pytest
from bs4 import BeautifulSoup

from novelsave_sources import Asset
from novelsave_sources.sources import Crawler


class MockCrawler(Crawler):
    pass


@pytest.fixture
def crawler():
    return MockCrawler()


@pytest.fixture
def html():
    return '''
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
</head>
<body>
    <main>
        <img src="https://website.com/image.jpg" alt="image">
    </main>
</body>
</html>
'''


def test_identify_assets(crawler, html):
    soup = BeautifulSoup(html, 'html.parser')

    assets = crawler.identify_assets(soup)

    expected_asset = Asset(
        name='image',
        url='https://website.com/image.jpg',
        mimetype='image/jpeg',
    )

    assert len(assets) == 1
    assert expected_asset == assets[0]
