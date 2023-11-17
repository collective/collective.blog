from Acquisition import aq_parent
from collective.blog.behaviors.blog import IBlogInfo
from plone import api
from plone.dexterity.content import DexterityContent
from Products.CMFPlone.Portal import IPloneSiteRoot


def _find_blog_uid(obj: DexterityContent) -> str:
    """Find a blog."""
    if IBlogInfo.providedBy(obj):
        return api.content.get_uuid(obj)
    elif IPloneSiteRoot.providedBy(obj):
        # No blog was found
        return "No blog was found."
    else:
        # Up one level (get parent)
        return _find_blog_uid(aq_parent(obj))
