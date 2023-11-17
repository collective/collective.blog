from Acquisition import aq_parent
from collective.blog.content.post import IPost
from collective.blog.content.post import Post
from collective.blog.indexers import _find_blog_uid
from plone.indexer import indexer


@indexer(IPost)
def blog_post_indexer(obj: Post):
    """Return blog uuid."""
    parent = aq_parent(obj)
    return _find_blog_uid(parent)
