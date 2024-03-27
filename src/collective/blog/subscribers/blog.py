from collective.blog import _
from collective.blog import logger
from collective.blog import PACKAGE_NAME
from collective.blog.content.blog import Blog
from plone import api
from zope.i18nmessageid.message import Message

import uuid


_AUTHORS_FOLDERISH = {
    "id": _("authors_folder_id", default="authors"),
    "title": _("authors_folder_title", default="Authors"),
    "description": _("authors_folder_desc", default="Our Authors"),
}

_TAGS_FOLDERISH = {
    "id": _("tags_folder_id", default="tags"),
    "title": _("tags_folder_title", default="Tags"),
    "description": _("tags_folder_desc", default=""),
}

PERMISSIONS_BLOG = (
    ("collective.blog: Add Blog", []),
    ("collective.blog: Add Author", []),
    ("collective.blog: Add Tag", []),
    (
        "collective.blog: Add Post",
        [
            "Manager",
            "Site Administrator",
            "Owner",
            "Editor",
            "Contributor",
        ],
    ),
)

PERMISSIONS_AUTHORS = (
    (
        "collective.blog: Add Author",
        ["Manager", "Site Administrator", "Owner", "Editor", "Contributor"],
    ),
)

PERMISSIONS_TAGS = (
    (
        "collective.blog: Add Tag",
        ["Manager", "Site Administrator", "Owner", "Editor", "Contributor"],
    ),
)


def _translate(msg: Message, lang: str) -> str:
    """Translate the msg to the desired language.

    This is here due to a bug on api.portal.translate that expects the language code to be
    on a specific format.
    ref: https://github.com/plone/plone.api/issues/524
    """
    if "-" in lang:
        lang_ = lang[:2]
        cc = lang[-2:].upper()
        lang = f"{lang_}_{cc}"
    return api.portal.translate(msg, domain=PACKAGE_NAME, lang=lang)


def _log_permission_change(path: str, permission_id: str, roles: list):
    roles = ", ".join(roles)
    logger.info(f"{path}: Set {permission_id} to roles {roles}")


def handle_new_blog_added(blog: Blog, event):
    # Set local permissions
    for permission_id, roles in PERMISSIONS_BLOG:
        blog.manage_permission(permission_id, roles=roles, acquire=False)
        _log_permission_change(blog.absolute_url_path(), permission_id, roles)

    # Create authors container
    create_authors_container(blog)
    create_tags_container(blog)


def create_authors_container(blog: Blog):
    key = "collective.blog.settings.enable_authors_folder"
    enabled = api.portal.get_registry_record(key, default=True)
    if not enabled:
        logger.info("Ignoring Authors folder creation")
        return
    lang = blog.language
    authors = api.content.create(
        type="Document",
        id=_translate(_AUTHORS_FOLDERISH["id"], lang=lang),
        title=_translate(_AUTHORS_FOLDERISH["title"], lang=lang),
        description=_translate(_AUTHORS_FOLDERISH["description"], lang=lang),
        container=blog,
    )
    uuids = [str(uuid.uuid4()), str(uuid.uuid4())]
    authors.blocks = {uuids[0]: {"@type": "title"}, uuids[1]: {"@type": "slate"}}
    authors.blocks_layout = {"items": [uuids[0], uuids[1]]}

    authors_path = "/".join(authors.getPhysicalPath())
    logger.info(f"Created {authors.id} folder inside {blog.absolute_url_path()}")
    for permission_id, roles in PERMISSIONS_AUTHORS:
        authors.manage_permission(permission_id, roles=roles, acquire=False)
        _log_permission_change(authors_path, permission_id, roles)


def create_tags_container(blog: Blog):
    key = "collective.blog.settings.enable_tags_folder"
    enabled = api.portal.get_registry_record(key, default=True)
    if not enabled:
        logger.info("Ignoring Tags folder creation")
        return
    lang = blog.language
    tags = api.content.create(
        type="Document",
        id=_translate(_TAGS_FOLDERISH["id"], lang=lang),
        title=_translate(_TAGS_FOLDERISH["title"], lang=lang),
        description=_translate(_TAGS_FOLDERISH["description"], lang=lang),
        container=blog,
    )
    uuids = [str(uuid.uuid4()), str(uuid.uuid4())]
    tags.blocks = {uuids[0]: {"@type": "title"}, uuids[1]: {"@type": "slate"}}
    tags.blocks_layout = {"items": [uuids[0], uuids[1]]}

    tags_path = "/".join(tags.getPhysicalPath())
    logger.info(f"Created {tags.id} folder inside {blog.absolute_url_path()}")
    for permission_id, roles in PERMISSIONS_TAGS:
        tags.manage_permission(permission_id, roles=roles, acquire=False)
        _log_permission_change(tags_path, permission_id, roles)

    return tags
