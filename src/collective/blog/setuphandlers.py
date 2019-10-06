# -*- coding: utf-8 -*-
from __future__ import absolute_import
from plone import api
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer
import logging

# The profile id of this package:
PROFILE_ID = 'profile-collective.blog:default'

INDEXES = (
    ("Summary", "FieldIndex"),
    )


@implementer(INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller"""
        return [
            'collective.blog:uninstall',
        ]


def post_install(context):
    """Post install script"""
    if context.readDataFile('collectiveblog_default.txt') is None:
        return

    add_catalog_indexes(context)


def uninstall(context):
    """Uninstall script"""
    if context.readDataFile('collectiveblog_uninstall.txt') is None:
        return

    remove_catalog_indexes(context)


def add_catalog_indexes(context, logger=None):
    """Method to add our wanted indexes to the portal_catalog.

    @parameters:

    When called from the import_various method below, 'context' is
    the plone site and 'logger' is the portal_setup logger.  But
    this method can also be used as upgrade step, in which case
    'context' will be portal_setup and 'logger' will be None.
    """
    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger('collective.blog')

    # Run the catalog.xml step as that may have defined new metadata
    # columns.  We could instead add <depends name="catalog"/> to
    # the registration of our import step in zcml, but doing it in
    # code makes this method usable as upgrade step as well.  Note that
    # this silently does nothing when there is no catalog.xml, so it
    # is quite safe.
    setup = api.portal.get_tool('portal_setup')
    setup.runImportStepFromProfile(PROFILE_ID, 'catalog')

    catalog = api.portal.get_tool('portal_catalog')
    indexes = catalog.indexes()

    indexables = []
    for name, meta_type in INDEXES:
        if name not in indexes:
            catalog.addIndex(name, meta_type)
            indexables.append(name)
            logger.info("Added %s for field %s.", meta_type, name)
    if len(indexables) > 0:
        logger.info("Indexing new indexes %s.", ', '.join(indexables))
        catalog.manage_reindexIndex(ids=indexables)


def remove_catalog_indexes(context):
    catalog = api.portal.get_tool('portal_catalog')
    indexes = catalog.indexes()

    for name, _ in INDEXES:
        if name in indexes:
            catalog.delIndex(name)
