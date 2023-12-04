from AccessControl.PermissionRole import rolesForPermissionOn
from collective.blog.content.blog import Blog
from copy import deepcopy
from plone import api
from plone.dexterity.content import DexterityContent
from plone.dexterity.fti import DexterityFTI
from zope.component import createObject

import pytest


CONTENT_TYPE = "BlogFolder"


@pytest.fixture
def blog(blogs: dict) -> Blog:
    """Return a blog instance."""
    blog_uuid = list(blogs.keys())[0]
    blog = api.content.get(UID=blog_uuid)
    return blog


@pytest.fixture
def authors_folder(blog: Blog) -> DexterityContent:
    """Return the authors folder created in a blog."""
    return blog["authors"]


@pytest.fixture
def disable_authors(portal):
    """Disable Authors folderish creation"""
    key = "collective.blog.settings.enable_authors_folder"
    api.portal.set_registry_record(key, False)
    yield portal
    api.portal.set_registry_record(key, True)


class TestBaseBlog:
    @pytest.fixture(autouse=True)
    def _fti(self, get_fti, integration, portal):
        self.fti = get_fti(CONTENT_TYPE)
        self.portal = portal


class TestBlog(TestBaseBlog):
    def test_fti(self):
        assert isinstance(self.fti, DexterityFTI)

    def test_factory(self):
        factory = self.fti.factory
        obj = createObject(factory)
        assert obj is not None
        assert isinstance(obj, Blog)

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
            "collective.blog.blog_info",
        ],
    )
    def test_has_behavior(self, get_behaviors, behavior):
        assert behavior in get_behaviors(CONTENT_TYPE)

    def test_create(self, blogs_payload):
        payload = blogs_payload[0]
        with api.env.adopt_roles(["Manager"]):
            content = api.content.create(container=self.portal, **payload)
        assert content.portal_type == CONTENT_TYPE
        assert isinstance(content, Blog)

    @pytest.mark.parametrize(
        "content_id,expected",
        [
            ("blog", "blog"),
            ("a-blog", "a-blog"),
            ("blog_name", "blog_name"),
            ("blog-folder", "blog-folder"),
            ("blog_folder", "blog_folder"),
            ("blogfolder", "blogfolder"),
        ],
    )
    def test_create_valid_ids(self, blogs_payload, content_id, expected):
        payload = deepcopy(blogs_payload[0])
        payload["id"] = content_id
        payload["safe_id"] = True
        with api.env.adopt_roles(["Manager"]):
            content = api.content.create(container=self.portal, **payload)
        assert content.id == expected

    def test_blog_info_behavior_applied(self, blog):
        from collective.blog.behaviors.blog import IBlogInfo

        assert IBlogInfo.providedBy(blog) is True

    def test_blog_info_behavior_indexed(self, blogs):
        from collective.blog.behaviors.blog import IBlogInfo

        brains = api.content.find(object_provides=IBlogInfo)

        assert len(brains) == 2


class TestBlogAuthorsFolder(TestBaseBlog):
    def test_authors_folder_creation(self, blogs_payload):
        payload = blogs_payload[0]
        with api.env.adopt_roles(["Manager"]):
            content = api.content.create(container=self.portal, **payload)
        assert "authors" in content.objectIds()

    @pytest.mark.parametrize(
        "attr,expected",
        [
            ["portal_type", "Document"],
            ["title", "Authors"],
        ],
    )
    def test_authors_folder(self, authors_folder, attr, expected):
        assert getattr(authors_folder, attr) == expected

    @pytest.mark.parametrize(
        "role",
        [
            "Manager",
            "Site Administrator",
            "Editor",
            "Contributor",
            "Owner",
        ],
    )
    def test_authors_folder_permission(self, authors_folder, role):
        permission = "collective.blog: Add Author"
        roles = rolesForPermissionOn(permission, authors_folder)
        assert role in roles

    def test_authors_folder_not_created(self, blogs_payload, disable_authors):
        payload = blogs_payload[0]
        with api.env.adopt_roles(["Manager"]):
            content = api.content.create(container=self.portal, **payload)
        assert "authors" not in content.objectIds()

    @pytest.mark.parametrize(
        "lang,o_id,o_title",
        [
            ("en", "authors", "Authors"),
            ("de", "autoren", "Autoren"),
            ("pt-br", "autores", "Autores"),
        ],
    )
    def test_authors_folder_translated(
        self, blogs_payload, lang: str, o_id: str, o_title: str
    ):
        payload = deepcopy(blogs_payload[0])
        payload["language"] = lang
        with api.env.adopt_roles(["Manager"]):
            content = api.content.create(container=self.portal, **payload)
        assert o_id in content.objectIds()
        assert content[o_id].title == o_title
