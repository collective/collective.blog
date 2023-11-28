from collective.blog.testing import ACCEPTANCE_TESTING
from collective.blog.testing import FUNCTIONAL_TESTING
from collective.blog.testing import INTEGRATION_TESTING
from copy import deepcopy
from plone import api
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.restapi.testing import RelativeSession
from pytest_plone import fixtures_factory

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
            "type": "Blog",
            "id": "tech-blog",
            "title": "Awesome Tech Blog",
            "description": "My awesome technical blog",
        },
        {
            "_container": "/",
            "type": "Blog",
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
    ]


@pytest.fixture
def blogs_payload(all_content, filter_items) -> list:
    """Payload to create two blogs items."""
    return filter_items(all_content, "Blog", True)


@pytest.fixture
def authors_payload(all_content, filter_items) -> list:
    """Payload to create two author items."""
    return filter_items(all_content, "Author", True)


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
def posts(portal, authors, blogs, posts_payload) -> dict:
    """Create Blogs, Authors and Posts."""
    response = {}
    authors_uuid = list(authors.keys())
    blog_uuid = list(blogs.keys())
    with api.env.adopt_roles(["Manager"]):
        blog = api.content.get(UID=blog_uuid[0])
        for data in posts_payload:
            # Add one author
            data["creators"] = [authors_uuid[0]]
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
