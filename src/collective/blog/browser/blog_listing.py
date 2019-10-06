from __future__ import absolute_import
import calendar
from six.moves.urllib.parse import quote_plus

from DateTime import DateTime
from Products.CMFPlone.PloneBatch import Batch
from Products.Five.browser import BrowserView
from plone import api
from plone.app.discussion.interfaces import IDiscussionSettings
from plone.app.discussion.interfaces import IConversation
from plone.app.event.base import default_timezone
from plone.memoize import view
from plone.memoize.instance import memoizedproperty
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from zope.component import queryUtility

from ..interfaces import IBlogSettings


class BlogListing(BrowserView):
    """Shows a Listing of all Blog entries, with the corresponding portlets.
    """

    filters = []

    def __init__(self, *args, **kwargs):
        super(BlogListing, self).__init__(*args, **kwargs)

        self.registry = queryUtility(IRegistry)

        req = self.request.form

        self.orphan = int(req.get('orphan', 1))
        self.b_start = int(req.get('b_start', 0))
        self.b_size = int(req.get('b_size', 0))
        if not self.b_size:
            registry = getUtility(IRegistry)
            self.b_size = registry.forInterface(
                IBlogSettings, check=False).batch_size or 0
        if not self.b_size:
            self.orphan = 0

        self.query = {}
        self.query['sort_on'] = 'Date'
        self.query['sort_order'] = 'reverse'
        self.query['portal_type'] = 'collective.blog.blogentry'
        self.query['path'] = '/'.join(self.context.getPhysicalPath())

        datefilter = self._get_datefilter_from_request()
        if datefilter:
            self.query['Date'] = {
                'query': (datefilter[0].earliestTime(),
                          datefilter[1].latestTime()),
                'range': 'minmax'}

        tags = req.get('tags')
        if tags:
            self.query['Subject'] = {'query': tags, 'operator': 'and'}

        searchable_text = req.get('searchable_text')
        if searchable_text:
            self.query['SearchableText'] = searchable_text

    def _get_datefilter_from_request(self):
        """ Calculates the date filter from
        the request

        It supports the following request Parameters:

            start   First blog entry date to search for
            end     Last blog entry date to search for, if omitted we will
                    use the current localized date.

            When you omit start and end you can give:

            year    The year so search for
            month   The month in the year above, can be omitted
            day     The day in the month and year above, can be omitted.

        @result: tuple with two DateTime objects (start, end) or None
        """

        timezone = default_timezone(context=self.context, as_tzinfo=False)

        req = self.request.form

        start = req.get('start', None)
        end = req.get('end', None)

        year = int(req.get('year', 0))
        month = int(req.get('month', 0))
        day = int(req.get('day', 0))

        result_start = None
        result_end = None
        if start and not end:
            try:
                result_start = DateTime(start)
                result_end = DateTime(timezone)
            except DateTime.SyntaxError:
                pass
        elif start and end:
            try:
                result_start = DateTime(start)
                result_end = DateTime(end)
            except DateTime.SyntaxError:
                result_start = None
                result_end = None

        elif day and month and year:
            result_start = DateTime("%s/%2.2d/%2.2d" % (year, month, day))
            result_end = DateTime("%s/%2.2d/%2.2d" % (year, month, day))
        elif month and year:
            result_start = DateTime("%s/%2.2d/%2.2d" % (year, month, 1))
            result_end = DateTime("%s/%2.2d/%2.2d" % (
                year,
                month,
                calendar.monthrange(year, month)[1]
            ))
        elif year:
            result_start = DateTime("%s/%2.2d/%2.2d" % (year, 1, 1))
            result_end = DateTime("%s/%2.2d/%2.2d" % (
                year,
                12,
                calendar.monthrange(year, 12)[1]
            ))

        if result_start and result_end:
            return (result_start, result_end)

        return None

    @view.memoize
    def entries(self):
        cat = api.portal.get_tool('portal_catalog')
        entries = cat(**self.query)

        batch = Batch(entries, self.b_size, self.b_start, orphan=self.orphan)

        return batch

    def query_string(self, **args):
        """Updates the query string of the current request with the given
        keyword arguments and returns it as a quoted string.
        """
        query = self.request.form.copy()
        # Remove empty query parameters
        for k, v in query.items():
            if v == '':
                del query[k]
        query.update(args)
        return '&'.join(["%s=%s" % (quote_plus(str(k)), quote_plus(str(v)))
                         for k, v in query.items()])

    def creatorOf(self, item):
        member = api.user.get(username=item.Creator)
        if member:
            return {
                'id': member.id,
                'name': member.getProperty('fullname') or member.id}
        return None

    @property
    def comments_enabled(self):
        # Check if discussion is allowed globally
        settings = self.registry.forInterface(IDiscussionSettings, check=False)
        if not settings.globally_enabled:
            return False

        # Check if discussion is allowed on the content type.
        portal_types = api.portal.get_tool('portal_types')
        document_fti = getattr(portal_types, 'collective.blog.blogentry')
        if not document_fti.getProperty('allow_discussion'):
            return False

        return True

    def amount_of_replies(self, brain):
        obj = brain.getObject()
        conversation = IConversation(obj)
        return len([thread for thread in conversation.getThreads()])

    @memoizedproperty
    def settings(self):
        settings = getUtility(IRegistry).forInterface(
            IBlogSettings, check=False)

        return settings
