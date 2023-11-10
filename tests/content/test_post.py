from collective.blog.content.post import Post
from plone import api
from plone.dexterity.fti import DexterityFTI
from zope.component import createObject

import pytest


CONTENT_TYPE = "Post"


class TestPost:
    @pytest.fixture(autouse=True)
    def _fti(self, get_fti, portal, blogs_payload):
        self.fti = get_fti(CONTENT_TYPE)
        with api.env.adopt_roles(["Manager"]):
            self.blog = api.content.create(container=portal, **blogs_payload[0])

    def test_fti(self):
        assert isinstance(self.fti, DexterityFTI)

    def test_factory(self):
        factory = self.fti.factory
        obj = createObject(factory)
        assert obj is not None
        assert isinstance(obj, Post)

    @pytest.mark.parametrize(
        "behavior",
        [
            "plone.basic",
            "plone.categorization",
            "plone.allowdiscussion",
            "plone.publication",
            "plone.namefromtitle",
            "plone.shortname",
            "plone.excludefromnavigation",
            "plone.relateditems",
            "plone.versioning",
            "volto.blocks",
            "volto.navtitle",
            "volto.preview_image_link",
            "volto.head_title",
        ],
    )
    def test_has_behavior(self, get_behaviors, behavior):
        assert behavior in get_behaviors(CONTENT_TYPE)

    def test_create(self, portal, posts_payload):
        """A Post need to be created inside a Blog."""
        blog = self.blog
        payload = posts_payload[0]
        with api.env.adopt_roles(["Manager"]):
            content = api.content.create(container=blog, **payload)
        assert content.portal_type == CONTENT_TYPE
        assert isinstance(content, Post)
