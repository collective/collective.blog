from collective.blog import utils
from plone.dexterity.content import Container
from zope.interface import implementer
from zope.interface import Interface


class IBlogTag(Interface):
    """A blog tag."""


@implementer(IBlogTag)
class BlogTag(Container):
    """An blog tag."""

    def blog_uid(self):
        """Return the uid of the nearest blog object."""
        return utils.find_blog_container_uid(self)
