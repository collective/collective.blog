from collective.blog.testing import ACCEPTANCE_TESTING
from collective.blog.testing import FUNCTIONAL_TESTING
from collective.blog.testing import INTEGRATION_TESTING
from copy import deepcopy
from pathlib import Path
from plone import api
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.restapi.testing import RelativeSession
from pytest_plone import fixtures_factory
from pythongettext.msgfmt import Msgfmt
from pythongettext.msgfmt import PoSyntaxError
from typing import Generator

import pytest


pytest_plugins = ["pytest_plone"]


globals().update(
    fixtures_factory(
        (
            (ACCEPTANCE_TESTING, "acceptance"),
            (FUNCTIONAL_TESTING, "functional"),
            (INTEGRATION_TESTING, "integration"),
        )
    )
)


@pytest.fixture(scope="session", autouse=True)
def generate_mo():
    """Generate .mo files."""
    import collective.blog

    locales_path = Path(collective.blog.__file__).parent / "locales"
    po_files: Generator = locales_path.glob("**/*.po")
    for po_file in po_files:
        parent: Path = po_file.parent
        domain: str = po_file.name[: -len(po_file.suffix)]
        mo_file: Path = parent / f"{domain}.mo"
        try:
            mo = Msgfmt(f"{po_file}", name=domain).getAsFile()
        except PoSyntaxError:
            continue
        else:
            with open(mo_file, "wb") as f_out:
                f_out.write(mo.read())


@pytest.fixture
def filter_items():
    def func(content: list, portal_type: str, only_public: bool = False) -> list:
        response = []
        for raw_item in content:
            if raw_item["type"] != portal_type:
                continue
            if only_public:
                item = {k: v for k, v in raw_item.items() if not k.startswith("_")}
            else:
                item = deepcopy(raw_item)
            response.append(item)
        return response

    return func


@pytest.fixture
def all_content() -> list:
    """Payload to create all content items."""
    return [
        {
            "_container": "/",
            "type": "Image",
            "id": "an-image",
            "title": "A Random Image",
            "description": "With some details",
            "_image": b"iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAAXNSR0IArs4c6QAAAA1JREFUGFdjCDO+/R8ABKsCZD++CcMAAAAASUVORK5CYII=",  # noQA
        },
        {
            "_container": "/",
            "type": "BlogFolder",
            "id": "tech-blog",
            "title": "Awesome Tech Blog",
            "description": "My awesome technical blog",
        },
        {
            "_container": "/",
            "type": "BlogFolder",
            "id": "dumpster",
            "title": "General",
            "description": "Posts about life, universe and everything",
        },
        {
            "_container": "/tech-blog/authors",
            "_preview_image_link": "/an-image",
            "type": "Author",
            "id": "douglas-adams",
            "title": "Douglas Adams",
            "description": "A very good writer",
        },
        {
            "_container": "/tech-blog/authors",
            "_preview_image_link": "/an-image",
            "type": "Author",
            "id": "marvin",
            "title": "Marvin",
            "description": "A very good nice robot",
        },
        {
            "_container": "/tech-blog",
            "_preview_image_link": "/an-image",
            "type": "Post",
            "id": "initial-commit",
            "title": "Initial Blog Post",
            "description": "Let's start my blog post with something cool",
        },
        {
            "_container": "/tech-blog",
            "_preview_image_link": "/an-image",
            "type": "Post",
            "id": "collective-blog",
            "title": "New package: collective.blog",
            "description": "This is a new cool package for Plone",
        },
        {
            "_container": "/tech-blog/tags",
            "_preview_image_link": "/an-image",
            "type": "BlogTag",
            "id": "retrocomputing",
            "title": "Retrocomputing",
            "description": "Posts about retrocomputing",
        },
    ]


@pytest.fixture
def blogs_payload(all_content, filter_items) -> list:
    """Payload to create two blogs items."""
    return filter_items(all_content, "BlogFolder", True)


@pytest.fixture
def authors_payload(all_content, filter_items) -> list:
    """Payload to create two author items."""
    return filter_items(all_content, "Author", True)


@pytest.fixture
def tags_payload(all_content, filter_items) -> list:
    """Payload to create a tag item."""
    return filter_items(all_content, "BlogTag", True)


@pytest.fixture
def posts_payload(all_content, filter_items) -> list:
    """Payload to create two posts items."""
    return filter_items(all_content, "Post", True)


@pytest.fixture
def blogs(portal, blogs_payload) -> dict:
    """Create Blogs content items."""
    response = {}
    with api.env.adopt_roles(["Manager"]):
        for data in blogs_payload:
            content = api.content.create(container=portal, **data)
            response[content.UID()] = content.title
    return response


@pytest.fixture
def authors(blogs, authors_payload) -> dict:
    """Create Authors content items."""
    response = {}
    blog_uuid = list(blogs.keys())
    with api.env.adopt_roles(["Manager"]):
        blog = api.content.get(UID=blog_uuid[0])
        authors = blog.authors
        for data in authors_payload:
            content = api.content.create(container=authors, **data)
            response[content.UID()] = content.title
    return response


@pytest.fixture
def tags(blogs, tags_payload) -> dict:
    """Create BlogTag content items."""
    response = {}
    blog_uuid = list(blogs.keys())
    with api.env.adopt_roles(["Manager"]):
        blog = api.content.get(UID=blog_uuid[0])
        tags = blog.tags
        for data in tags_payload:
            content = api.content.create(container=tags, **data)
            response[content.UID()] = content.title
    return response


@pytest.fixture
def posts(portal, authors, tags, blogs, posts_payload) -> dict:
    """Create Blogs, Authors and Posts."""
    response = {}
    authors_uuid = list(authors.keys())
    blog_uuid = list(blogs.keys())
    tags_uuid = list(tags.keys())
    with api.env.adopt_roles(["Manager"]):
        blog = api.content.get(UID=blog_uuid[0])
        for data in posts_payload:
            # Add one author and one tag
            data["creators"] = [authors_uuid[0]]
            data["blog_tags"] = [tags_uuid[0]]
            content = api.content.create(container=blog, **data)
            response[content.UID()] = content.title
    return response


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
