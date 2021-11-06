import pytest
from requests import Response
from requests.cookies import RequestsCookieJar

from novelsave_sources import BaseHttpGateway, novel_source_types, UnavailableException


class MockGateway(BaseHttpGateway):
    class RequestException(Exception):
        pass

    def request(
        self,
        method: str,
        url: str,
        headers: dict = None,
        params: dict = None,
        data: dict = None,
        json: dict = None,
    ) -> Response:
        raise self.RequestException()

    @property
    def cookies(self) -> RequestsCookieJar:
        pass


@pytest.fixture
def gateway():
    return MockGateway()


@pytest.mark.parametrize("source_type", novel_source_types())
def test_novel_source_should_accept_http_gateway(source_type, gateway):
    source = source_type(gateway)
    assert source.http_gateway == gateway


@pytest.mark.parametrize("source_type", novel_source_types())
def test_novel_source_should_mark_search_viable(source_type, gateway):
    source = source_type(gateway)

    try:
        source.search("query")
    except MockGateway.RequestException:
        did_search = True
    except UnavailableException:
        did_search = False
    else:
        did_search = True

    assert source.search_viable == did_search
