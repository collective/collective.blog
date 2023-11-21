from plone import api


def auto_add_authors_container(obj, event):
    authors = api.content.create(
        type="Document",
        title="Authors",
        container=obj,
    )

    permission_id = "collective.blog: Add Author"
    roles = ["Manager", "Site Administrator", "Owner", "Editor", "Contributor"]
    authors.manage_permission(permission_id, roles=roles)
