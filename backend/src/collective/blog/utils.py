from Acquisition import aq_chain
from collective.blog.behaviors.blog import IBlogInfo
from plone import api
from plone.dexterity.content import DexterityContent


_BLOG_TYPES = ("BlogFolder",)


def find_blog_container_uid(obj: DexterityContent) -> str:
    """Find a blog."""
    for parent in aq_chain(obj):
        if (
            IBlogInfo.providedBy(parent)
            or getattr(parent, "portal_type", "") in _BLOG_TYPES
        ):
            return api.content.get_uuid(parent)
    return ""
