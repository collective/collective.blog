"""Module where all interfaces, events and exceptions live."""
from collective.blog import _
from zope import schema
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class IBrowserLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IBlogSettings(Interface):
    enable_authors_folder = schema.Bool(
        title=_("Authors container inside the Blog"),
        description=_(
            "help_enable_authors_folder",
            default="Should we create the Authors container inside the Blog?",
        ),
        required=False,
        default=True,
    )
