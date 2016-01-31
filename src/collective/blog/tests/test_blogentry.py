# -*- coding: utf-8 -*-
from plone.app.testing import TEST_USER_ID
from zope.component import queryUtility
from zope.component import createObject
from plone.app.testing import setRoles
from plone.dexterity.interfaces import IDexterityFTI
from plone import api

from collective.blog.testing import COLLECTIVE_BLOG_INTEGRATION_TESTING  # noqa
from collective.blog.interfaces import IBlogEntry

import unittest2 as unittest


class BlogEntryIntegrationTest(unittest.TestCase):

    layer = COLLECTIVE_BLOG_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='BlogEntry')
        schema = fti.lookupSchema()
        self.assertEqual(IBlogEntry, schema)

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='BlogEntry')
        self.assertTrue(fti)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='BlogEntry')
        factory = fti.factory
        obj = createObject(factory)
        self.assertTrue(IBlogEntry.providedBy(obj))

    def test_adding(self):
        self.portal.invokeFactory('BlogEntry', 'BlogEntry')
        self.assertTrue(
            IBlogEntry.providedBy(self.portal['BlogEntry'])
        )
