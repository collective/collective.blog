from collective.blog.content.author import Author
from plone import api
from plone.dexterity.fti import DexterityFTI
from zope.component import createObject

import pytest


CONTENT_TYPE = "Author"


class TestAuthor:
    @pytest.fixture(autouse=True)
    def _fti(self, get_fti, portal, blogs_payload):
        self.fti = get_fti(CONTENT_TYPE)
        with api.env.adopt_roles(["Manager"]):
            self.blog = api.content.create(container=portal, **blogs_payload[0])
            self.authors = self.blog.authors

    def test_fti(self):
        assert isinstance(self.fti, DexterityFTI)

    def test_factory(self):
        factory = self.fti.factory
        obj = createObject(factory)
        assert obj is not None
        assert isinstance(obj, Author)

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

    def test_create(self, portal, authors_payload):
        """A Blog Author need to be created inside a Blog authors folder."""
        authors_folder = self.authors
        payload = authors_payload[0]
        with api.env.adopt_roles(["Manager"]):
            content = api.content.create(container=authors_folder, **payload)
        assert content.portal_type == CONTENT_TYPE
        assert isinstance(content, Author)

    def test_create_fail(self, portal, authors_payload):
        """A Blog Author need to be created inside a Blog authors folder."""
        blog = self.blog
        payload = authors_payload[0]
        with pytest.raises(api.exc.InvalidParameterError) as exc:
            with api.env.adopt_roles(["Manager"]):
                api.content.create(container=blog, **payload)
        assert "Disallowed subobject type: Author" in str(exc)

    def test_indexer_blog(self, portal, authors_payload):
        blog = self.blog
        authors_folder = self.authors
        blog_uid = api.content.get_uuid(blog)
        payload = authors_payload[0]
        # Check there is no Author connected to this blog
        brains = api.content.find(portal_type=CONTENT_TYPE, blog=blog_uid)
        assert len(brains) == 0
        # Create an Author inside the blog
        with api.env.adopt_roles(["Manager"]):
            content = api.content.create(container=authors_folder, **payload)

        brains = api.content.find(portal_type=CONTENT_TYPE, blog=blog_uid)
        assert len(brains) == 1
        assert brains[0].Title == content.title
