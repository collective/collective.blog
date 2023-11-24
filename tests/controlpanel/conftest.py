import pytest


@pytest.fixture()
def portal(functional):
    portal = functional["portal"]
    return portal


@pytest.fixture()
def http_request(functional):
    return functional["request"]
