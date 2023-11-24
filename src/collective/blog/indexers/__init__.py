from Acquisition import aq_parent
from collective.blog.behaviors.blog import IBlogInfo
from plone import api
from plone.dexterity.content import DexterityContent
from Products.CMFPlone.Portal import IPloneSiteRoot


def _find_blog_uid(obj: DexterityContent) -> str:
    """Find a blog."""
    if IBlogInfo.providedBy(obj):
        return api.content.get_uuid(obj)
    else:
        # Up one level (get parent) if not reached the root of the site
        return "" if IPloneSiteRoot.providedBy(obj) else _find_blog_uid(aq_parent(obj))
