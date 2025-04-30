from collective.blog import _
from collective.blog.interfaces import IBlogSettings
from plone.restapi.controlpanels import RegistryConfigletPanel
from zope.component import adapter
from zope.interface import Interface


@adapter(Interface, Interface)
class BlogConfigletPanel(RegistryConfigletPanel):
    """Blog Settings Control Panel"""

    schema = IBlogSettings
    schema_prefix = "collective.blog.settings"
    configlet_id = "blog-controlpanel"
    configlet_category_id = "Products"
    title = _("Blog Settings")
    group = "Products"
