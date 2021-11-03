import pytest
from requests import Response
from requests.cookies import RequestsCookieJar

from novelsave_sources import BaseHttpGateway, novel_source_types


class MockGateway(BaseHttpGateway):
    def request(
        self,
        method: str,
        url: str,
        headers: dict = None,
        params: dict = None,
        data: dict = None,
        json: dict = None,
    ) -> Response:
        pass

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
