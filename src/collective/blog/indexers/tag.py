from collective.blog.content.tag import BlogTag
from collective.blog.content.tag import IBlogTag
from plone.indexer import indexer


@indexer(IBlogTag)
def blog_tag_indexer(obj: BlogTag):
    """Return blog uuid."""
    return obj.blog_uid()
