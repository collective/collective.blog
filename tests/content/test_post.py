from collective.blog.content.post import Post
from plone import api
from plone.dexterity.fti import DexterityFTI
from zope.component import createObject

import pytest


CONTENT_TYPE = "Post"


@pytest.fixture
def subfolder():
    def func(blog, year):
        payload = {
            "container": blog,
            "type": "Document",
            "id": f"{year}",
            "title": f"{year}",
            "description": f"Posts from {year}",
        }
        subfolder = api.content.create(**payload)
        return subfolder

    return func


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

    def test_will_not_create_root(self, portal, posts_payload):
        """A Post will not be created at the site Root."""
        from AccessControl import Unauthorized

        payload = posts_payload[0]
        with pytest.raises(Unauthorized) as exc:
            with api.env.adopt_roles(["Manager"]):
                api.content.create(container=portal, **payload)
        assert "Cannot create Post" in str(exc)

    def test_create(self, portal, posts_payload):
        """A Post need to be created inside a Blog."""
        blog = self.blog
        payload = posts_payload[0]
        with api.env.adopt_roles(["Manager"]):
            content = api.content.create(container=blog, **payload)
        assert content.portal_type == CONTENT_TYPE
        assert isinstance(content, Post)

    def test_create_inside_document(self, portal, posts_payload, subfolder):
        """A Post need to be created inside a subfolder of a Blog."""
        blog = self.blog
        payload = posts_payload[0]
        with api.env.adopt_roles(["Manager"]):
            container = subfolder(blog, 2024)
            content = api.content.create(container=container, **payload)
        assert content.portal_type == CONTENT_TYPE
        assert isinstance(content, Post)

    def test_query_posts_by_tag(self, tags_payload, posts_payload):
        blog = self.blog
        with api.env.adopt_roles(["Manager"]):
            tag = api.content.create(container=blog.tags, **tags_payload[0])
            api.content.create(
                container=blog, **posts_payload[0], blog_tags=[tag.UID()]
            )
        result = api.content.find(blog_tags=tag.UID())
        assert len(result) == 1
