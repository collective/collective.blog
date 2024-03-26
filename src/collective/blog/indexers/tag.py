from collective.blog.behaviors.tags import IBlogTags
from collective.blog.content.tag import BlogTag
from collective.blog.content.tag import IBlogTag
from plone.indexer import indexer


@indexer(IBlogTag)
def tag_blog_uid_indexer(obj: BlogTag):
    """Return blog uuid."""
    return obj.blog_uid()


@indexer(IBlogTags)
def blog_tags(obj: IBlogTags):
    """Returns the tags of a blog post."""
    return obj.blog_tags
