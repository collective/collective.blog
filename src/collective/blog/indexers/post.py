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
    for uid in uids:
        searchResult = api.content.find(portal_type="Author", UID=uid)
        if len(searchResult) > 0:
            author = searchResult[0].getObject()

            if author is not None:
                authors.append(author.title)

    return authors
