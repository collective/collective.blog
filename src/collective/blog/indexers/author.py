from Acquisition import aq_parent
from collective.blog.content.author import Author
from collective.blog.content.author import IAuthor
from collective.blog.indexers import _find_blog_uid
from plone.indexer import indexer


@indexer(IAuthor)
def blog_author_indexer(obj: Author):
    """Return blog uuid."""
    parent = aq_parent(obj)
    return _find_blog_uid(parent)
