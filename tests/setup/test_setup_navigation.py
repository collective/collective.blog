from plone import api

import pytest


class TestSetupNavigation:
    @pytest.fixture(autouse=True)
    def _init(self, portal):
        self.portal = portal

    @pytest.mark.parametrize(
        "portal_type",
        [
            "Author",
            "Blog",
            "Collection",
            "Document",
            "Event",
            "Folder",
            "Link",
            "News Item",
        ],
    )
    def test_type_allowed_in_navigation(self, portal_type: str):
        """Test if portal_type is listed in navigation."""
        key = "plone.displayed_types"
        values = api.portal.get_registry_record(key)
        assert portal_type in values
