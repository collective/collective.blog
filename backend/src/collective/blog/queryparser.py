from collections import namedtuple
from plone import api


Row = namedtuple("Row", ["index", "operator", "values"])
PATH_INDICES = {"path"}


def currentUID(context, row):
    """Current object UID"""
    uid = api.content.get_uuid(context)
    return {row.index: {"query": uid}}
