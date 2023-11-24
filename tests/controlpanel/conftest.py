from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.restapi.testing import RelativeSession

import pytest


@pytest.fixture()
def app(functional):
    return functional["app"]


@pytest.fixture()
def portal(functional):
    portal = functional["portal"]
    return portal


@pytest.fixture()
def http_request(functional):
    return functional["request"]


@pytest.fixture()
def request_factory(portal):
    def factory():
        url = portal.absolute_url()
        api_session = RelativeSession(url)
        api_session.headers.update({"Accept": "application/json"})
        return api_session

    return factory


@pytest.fixture()
def anon_request(request_factory):
    return request_factory()


@pytest.fixture()
def manager_request(request_factory):
    request = request_factory()
    request.auth = (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)
    yield request
    request.auth = ()
