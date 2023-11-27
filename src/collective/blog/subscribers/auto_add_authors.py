from plone import api

import uuid


def auto_add_authors_container(obj, event):
    authors = api.content.create(
        type="Document",
        title="Authors",
        container=obj,
    )

    uuids = [str(uuid.uuid4()), str(uuid.uuid4())]
    authors.blocks = {uuids[0]: {"@type": "title"}, uuids[1]: {"@type": "slate"}}
    authors.blocks_layout = {"items": [uuids[0], uuids[1]]}

    permission_id = "collective.blog: Add Author"
    roles = ["Manager", "Site Administrator", "Owner", "Editor", "Contributor"]
    authors.manage_permission(permission_id, roles=roles)
