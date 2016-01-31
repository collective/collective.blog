# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.blog.testing import COLLECTIVE_BLOG_INTEGRATION_TESTING  # noqa
from plone import api

import unittest


class TestSetup(unittest.TestCase):
    """Test that collective.blog is properly installed."""

    layer = COLLECTIVE_BLOG_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if collective.blog is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'collective.blog'))

    def test_browserlayer(self):
        """Test that ICollectiveBlogLayer is registered."""
        from collective.blog.interfaces import (
            ICollectiveBlogLayer)
        from plone.browserlayer import utils
        self.assertIn(ICollectiveBlogLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = COLLECTIVE_BLOG_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['collective.blog'])

    def test_product_uninstalled(self):
        """Test if collective.blog is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'collective.blog'))

    def test_browserlayer_removed(self):
        """Test that ICollectiveBlogLayer is removed."""
        from collective.blog.interfaces import ICollectiveBlogLayer
        from plone.browserlayer import utils
        self.assertNotIn(ICollectiveBlogLayer, utils.registered_layers())
