# -*- coding: utf-8 -*-
from __future__ import absolute_import
from plone import api
from plone.app.layout.viewlets import ViewletBase
from plone.memoize.instance import memoizedproperty
from plone.registry.interfaces import IRegistry
from collective.blog.interfaces import IBlogSettings
from zope.component import getUtility


class DocumentBylineViewlet(ViewletBase):

    def __init__(self, context, request, view, manager=None):
        super(DocumentBylineViewlet, self).__init__(
            context, request, view, manager
        )

    def show(self):
        return True

    def review_state(self):
        wftool = api.portal.get_tool("portal_workflow")
        return wftool.getInfoFor(self.context, 'review_state')

    def creator(self):
        member = api.user.get(username=self.context.Creator())
        if member:
            return {
                'id': member.id,
                'name': member.getProperty('fullname') or member.id}
        return None

    @memoizedproperty
    def settings(self):
        settings = getUtility(IRegistry).forInterface(
            IBlogSettings, check=False)

        return settings
