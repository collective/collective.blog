from collective.blog.content.author import Author
from collective.blog.content.author import IAuthor
from plone.indexer import indexer


@indexer(IAuthor)
def blog_author_indexer(obj: Author):
    """Return blog uuid."""
    return obj.blog_uid()
