from collective.blog.content.post import IPost
from collective.blog.content.post import Post
from plone.indexer import indexer


@indexer(IPost)
def blog_post_indexer(obj: Post):
    """Return blog uuid."""
    return obj.blog_uid()
