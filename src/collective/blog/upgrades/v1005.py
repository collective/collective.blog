from collective.blog.interfaces import IBlogSettings
from plone.registry.interfaces import IRegistry
from zope.component import getUtility


def update_registry_records(self):
    # add new persistent setting in registry
    registry = getUtility(IRegistry)
    registry.registerInterface(IBlogSettings)
