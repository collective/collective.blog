from plone.dexterity.content import Container
from zope.interface import implementer
from zope.interface import Interface


class IBlog(Interface):
    """A Blog."""


@implementer(IBlog)
class Blog(Container):
    """A Blog."""
