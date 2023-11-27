from collective.blog.content.blog import Blog
from collective.blog.upgrades.v1002 import TYPES_MAPPING
from copy import deepcopy
from plone import api
from plone.dexterity.fti import DexterityFTI

import pytest


@pytest.fixture
def modify_ftis(portal, get_fti):
    """Modify fti"""

    def func():
        with api.env.adopt_roles(["Manager"]):
            # Rename new content type back to its old name
            types_tool = portal.portal_types
            for old_pt, new_pt in TYPES_MAPPING:
                types_tool.manage_renameObject(new_pt, old_pt)
                fti = get_fti(old_pt)
                fti.title = old_pt

    return func


@pytest.fixture
def old_blog_factory(portal, blogs_payload):
    def func() -> Blog:
        with api.env.adopt_roles(["Manager"]):
            payload = deepcopy(blogs_payload[0])
            payload["type"] = "Blog"
            payload["id"] = "old-blog"
            return api.content.create(portal, **payload)

    return func


class TestUpgradeV1002:
    src: str = "1001"
    dest: str = "1002"

    @pytest.fixture(autouse=True)
    def _init(self, get_fti, do_rollback, do_upgrade, modify_ftis, old_blog_factory):
        do_rollback(self.src)
        modify_ftis()
        self.get_fti = get_fti
        self.old_blog = old_blog_factory()
        self.upgrade = do_upgrade

    def test_blog_fti_available_in_1001(self):
        assert isinstance(self.get_fti("Blog"), DexterityFTI)
        assert self.get_fti("BlogFolder") is None

    def test_blogfolder_fti_available_in_1002(self, do_upgrade):
        do_upgrade(self.dest)
        assert isinstance(self.get_fti("BlogFolder"), DexterityFTI)
        assert self.get_fti("Blog") is None

    def test_old_blogs_migrated(self, do_upgrade):
        with api.env.adopt_roles(["Manager"]):
            brains = api.content.find(portal_type="BlogFolder")
        assert len(brains) == 0
        # Upgrade
        do_upgrade(self.dest)
        with api.env.adopt_roles(["Manager"]):
            brains = api.content.find(portal_type="BlogFolder")
        assert len(brains) == 1
        assert self.old_blog.portal_type == "BlogFolder"
        assert self.old_blog.Type() == "BlogFolder"
