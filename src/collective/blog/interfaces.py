# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from zope import schema
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer

from . import _


class ICollectiveBlogLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IBlogSettings(Interface):
    """ Marker Interface for Registry Settings of this
    Addon.
    """

    show_lead_image = schema.Bool(
        title=_(u"Show lead image in blog entries"),
        default=False)

    batch_size = schema.Int(
        title=_(u"Number of blog entries to show on "
                u"batch (prev/next) navigations"),
        default=10)

    show_folder_title = schema.Bool(
        title=_(u"Show the folders title on blog listings"),
        default=False)

    allow_anonymous_view_about = schema.Bool(
        title=_(u"Allow anonymous users to see the about line"),
        default=False)


class IBlogEntryView(Interface):
    """Marker Interface for BlogView
    """
