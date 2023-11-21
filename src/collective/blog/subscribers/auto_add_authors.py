from plone import api


def auto_add_authors_container(obj, event):
    api.content.create(type="Authors", title="Authors", container=obj)
