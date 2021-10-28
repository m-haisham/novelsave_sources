import pytest
from requests import Response
from requests.cookies import RequestsCookieJar

from novelsave_sources import BaseHttpGateway
from novelsave_sources import metadata_source_types


class MockGateway(BaseHttpGateway):
    def request(self, method: str, url: str, headers: dict = None, params: dict = None, data: dict = None,
                json: dict = None) -> Response:
        pass

    @property
    def cookies(self) -> RequestsCookieJar:
        pass


@pytest.fixture
def gateway():
    return MockGateway()


@pytest.mark.parametrize('source_type', metadata_source_types())
def test_all_metadata_sources_should_receive_http_gateway(source_type, gateway):
    source = source_type(gateway)
    assert source.http_gateway == gateway
