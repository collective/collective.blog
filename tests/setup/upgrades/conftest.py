from collective.blog import PACKAGE_NAME
from plone import api

import pytest


PROFILE_ID = f"profile-{PACKAGE_NAME}:default"


@pytest.fixture
def do_rollback(portal):
    """Rollback profile config."""

    def func(src: str):
        with api.env.adopt_roles(["Manager"]):
            setup_tool = portal.portal_setup
            setup_tool.setLastVersionForProfile(PROFILE_ID, src)

    return func


@pytest.fixture
def do_upgrade(portal):
    def func(dest: str):
        with api.env.adopt_roles(["Manager"]):
            setup_tool = portal.portal_setup
            setup_tool.upgradeProfile(PROFILE_ID, dest=dest)

    return func
