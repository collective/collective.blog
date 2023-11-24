from collective.blog import logger
from collective.blog.content.blog import Blog
from plone import api


PERMISSIONS_BLOG = (
    ("collective.blog: Add Blog", []),
    ("collective.blog: Add Author", []),
)
PERMISSIONS_AUTHORS = (
    (
        "collective.blog: Add Author",
        ["Manager", "Site Administrator", "Owner", "Editor", "Contributor"],
    ),
)


def _log_permission_change(path: str, permission_id: str, roles: list):
    roles = ", ".join(roles)
    logger.info(f"{path}: Set {permission_id} to roles {roles}")


def auto_add_authors_container(blog: Blog, event):
    key = "collective.blog.settings.enable_authors_folder"
    enabled = api.portal.get_registry_record(key, default=True)
    if not enabled:
        logger.info("Ignoring Authors folder creation")
        return
    blog_path = "/".join(blog.getPhysicalPath())
    for permission_id, roles in PERMISSIONS_BLOG:
        blog.manage_permission(permission_id, roles=roles, acquire=False)
        _log_permission_change(blog_path, permission_id, roles)
    authors = api.content.create(
        type="Document",
        id="authors",
        title="Authors",
        container=blog,
    )
    authors_path = "/".join(authors.getPhysicalPath())
    logger.info(f"Created authors folder inside {blog_path}")
    for permission_id, roles in PERMISSIONS_AUTHORS:
        authors.manage_permission(permission_id, roles=roles, acquire=False)
        _log_permission_change(authors_path, permission_id, roles)
