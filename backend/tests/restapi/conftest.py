from base64 import b64decode
from copy import deepcopy
from plone import api
from plone.namedfile.file import NamedBlobImage

import pytest
import transaction


@pytest.fixture()
def create_content_tree(all_content):
    def func():
        contents = []
        author_uid = ""
        with api.env.adopt_roles(["Manager"]):
            # Create image to be used as preview
            for data in all_content:
                item = deepcopy(data)
                target_info = None
                parent = item.pop("_container")
                container = api.content.get(path=parent)
                if "_image" in item:
                    item["image"] = NamedBlobImage(b64decode(item.pop("_image")))
                if "_preview_image_link" in item:
                    target_info = (
                        api.content.get(item.pop("_preview_image_link")),
                        "preview_image_link",
                    )
                if item["type"] == "Post":
                    item["creators"] = [author_uid]
                content = api.content.create(container=container, **item)
                if target_info:
                    target, relationship = target_info
                    api.relation.create(content, target, relationship)
                content_uid = api.content.get_uuid(content)
                if item["type"] == "Author" and not author_uid:
                    author_uid = content_uid
                contents.append(content_uid)
        return contents

    return func


@pytest.fixture()
def portal(functional, create_content_tree):
    portal = functional["portal"]
    with transaction.manager:
        contents = create_content_tree()
    yield portal
    with transaction.manager:
        for uid in contents[::-1]:
            obj = api.content.get(UID=uid)
            if obj:
                api.content.delete(obj)


@pytest.fixture()
def http_request(functional):
    return functional["request"]
