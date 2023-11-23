from collective.blog.testing import ACCEPTANCE_TESTING
from collective.blog.testing import FUNCTIONAL_TESTING
from collective.blog.testing import INTEGRATION_TESTING
from plone import api
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
def blogs_payload() -> list:
    """Payload to create two blogs items."""
    return [
        {
            "type": "Blog",
            "id": "tech-blog",
            "title": "Awesome Tech Blog",
            "description": "My awesome technical blog",
        },
        {
            "type": "Blog",
            "id": "dumpster",
            "title": "General",
            "description": "Posts about life, universe and everything",
        },
    ]


@pytest.fixture
def authors_payload() -> list:
    """Payload to create two author items."""
    return [
        {
            "type": "Author",
            "id": "douglas-adams",
            "title": "Douglas Adams",
            "description": "A very good writer",
        },
        {
            "type": "Author",
            "id": "marvin",
            "title": "Marvin",
            "description": "A very good nice robot",
        },
    ]


@pytest.fixture
def posts_payload() -> list:
    """Payload to create two posts items."""
    return [
        {
            "type": "Post",
            "id": "initial-commit",
            "title": "Initial Blog Post",
            "description": "Let's start my blog post with something cool",
        },
        {
            "type": "Post",
            "id": "collective-blog",
            "title": "New package: collective.blog",
            "description": "This is a new cool package for Plone",
        },
    ]


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
