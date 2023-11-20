from plone.dexterity.content import Container
from zope.interface import implementer
from zope.interface import Interface


class IAuthors(Interface):
    """An Authors folder."""


@implementer(IAuthors)
class Authors(Container):
    """An Author."""
