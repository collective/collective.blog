from collective.blog.content.post import IPost
from collective.blog.content.post import Post
from plone import api
from plone.indexer import indexer


@indexer(IPost)
def blog_post_indexer(obj: Post):
    """Return blog uuid."""
    return obj.blog_uid()


@indexer(IPost)
def post_authors(obj: Post):
    """Returns the authors of a blog post."""
    authors = []
    uids = obj.creators
    brains = api.content.find(portal_type="Author", UID=uids)
    for brain in brains:
        authors.append(brain.Title)
    return authors
