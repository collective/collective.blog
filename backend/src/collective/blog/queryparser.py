from collections import namedtuple
from Products.CMFCore.utils import getToolByName


Row = namedtuple("Row", ["index", "operator", "values"])
PATH_INDICES = {"path"}


def _currentUID(context, row):
    """Current user lookup"""
    # placeholder
    mt = getToolByName(context, "portal_membership")
    user = mt.getAuthenticatedMember()
    return {row.index: {"query": user.getId()}}
