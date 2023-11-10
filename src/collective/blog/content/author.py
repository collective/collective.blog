from plone.dexterity.content import Container
from zope.interface import implementer
from zope.interface import Interface


class IAuthor(Interface):
    """An Author."""


@implementer(IAuthor)
class Author(Container):
    """An Author."""
