from collective.blog.content.tag import BlogTag
from plone import api
from plone.dexterity.fti import DexterityFTI
from zope.component import createObject

import pytest


CONTENT_TYPE = "BlogTag"


class TestBlogTag:
    @pytest.fixture(autouse=True)
    def _fti(self, get_fti, portal, blogs_payload):
        self.fti = get_fti(CONTENT_TYPE)
        with api.env.adopt_roles(["Manager"]):
            self.blog = api.content.create(container=portal, **blogs_payload[0])
            self.tags = self.blog.tags

    def test_fti(self):
        assert isinstance(self.fti, DexterityFTI)

    def test_factory(self):
        factory = self.fti.factory
        obj = createObject(factory)
        assert obj is not None
        assert isinstance(obj, BlogTag)

    @pytest.mark.parametrize(
        "behavior",
        [
            "plone.dublincore",
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

    def test_create(self, portal, tags_payload):
        """A Blog Tag needs to be created inside a Blog tags folder."""
        tags_folder = self.tags
        payload = tags_payload[0]
        with api.env.adopt_roles(["Manager"]):
            content = api.content.create(container=tags_folder, **payload)
        assert content.portal_type == CONTENT_TYPE
        assert isinstance(content, BlogTag)

    def test_create_fail(self, portal, tags_payload):
        """A Blog Tag needs to be created inside a Blog tags folder."""
        blog = self.blog
        payload = tags_payload[0]
        with pytest.raises(api.exc.InvalidParameterError) as exc:
            with api.env.adopt_roles(["Manager"]):
                api.content.create(container=blog, **payload)
        assert "Disallowed subobject type: BlogTag" in str(exc)

    def test_indexer_blog(self, portal, tags_payload):
        blog = self.blog
        tags_folder = self.tags
        blog_uid = api.content.get_uuid(blog)
        payload = tags_payload[0]
        # Check there is no BlogTag connected to this blog
        brains = api.content.find(portal_type=CONTENT_TYPE, blog_uid=blog_uid)
        assert len(brains) == 0
        # Create a BlogTag inside the blog
        with api.env.adopt_roles(["Manager"]):
            content = api.content.create(container=tags_folder, **payload)

        brains = api.content.find(portal_type=CONTENT_TYPE, blog_uid=blog_uid)
        assert len(brains) == 1
        assert brains[0].Title == content.title
        assert brains[0].blog_uid == blog_uid
