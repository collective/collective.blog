# -*- coding: utf-8 -*-
from __future__ import absolute_import
from zope.interface import implementer

from Products.Five import BrowserView
from plone.memoize.instance import memoizedproperty
from plone.registry.interfaces import IRegistry
from collective.blog.interfaces import IBlogEntryView
from zope.component import getUtility

from ..interfaces import IBlogSettings


@implementer(IBlogEntryView)
class BlogEntryView(BrowserView):
    """The Blog entry detail View."""

    def __init__(self, context, request):
        super(BlogEntryView, self).__init__(context, request)

    @memoizedproperty
    def settings(self):
        settings = getUtility(IRegistry).forInterface(
            IBlogSettings, check=False)

        return settings
