# -*- coding: utf-8 -*-
from __future__ import absolute_import
from decimal import Decimal
import re
from zope import schema
from zope.interface import implementer

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone import api
from plone.app.contenttypes.interfaces import IFolder
from plone.app.event.base import find_ploneroot
from plone.app.event.base import find_site
from plone.app.portlets.portlets import base
from plone.app.uuid.utils import uuidToObject
from plone.app.vocabularies.catalog import CatalogSource
from plone.memoize.compress import xhtml_compress
from plone.memoize.instance import memoizedproperty
from plone.portlets.interfaces import IPortletDataProvider

from .. import _
import six


search_base_uid_source = CatalogSource(object_provides={
    'query': [
        IFolder.__identifier__
    ],
    'operator': 'or'
})


class ITagsPortlet(IPortletDataProvider):

    header = schema.TextLine(
        title=_(u'portlet_tags_title_label',
                default=u"Portlet header"),
        description=_(u'portlet_tags_title_help',
                      default=u"Title of the rendered portlet"),
        constraint=re.compile(r"[^\s]").match,
        required=False)

    maxsize = schema.Decimal(title=_(u'portlet_tags_maxsize_label',
                                     default=u'Max. Fontsize'),
                             description=_(u'portlet_tags_maxsize_help',
                                           default=u'Size in em'),
                             required=True,
                             default=Decimal(2.0))

    minsize = schema.Decimal(title=_(u'portlet_tags_minsize_label',
                                     default=u'Min. Fontsize'),
                             description=_(u'portlet_tags_minsize_help',
                                           default=u'Size in em'),
                             required=True,
                             default=Decimal(0.7))

    footer = schema.TextLine(
        title=_(u'portlet_tags_footer_label', default=u"Portlet footer"),
        description=_(u'portlet_tags_footer_help',
                      default=u"Text to be shown in the footer"),
        required=False)

    search_base_uid = schema.Choice(
        title=_(u'portlet_tags_search_base_label', default=u'Search base'),
        description=_(
            u'portlet_tags_search_base_help',
            default=u'Select search base Folder to search for '
                    u'tags. The URL to to this item will also be used to '
                    u'link to in tag searches. If empty, the whole site '
                    u'will be searched and the tag cloud view will be '
                    u'called on the site root.'
        ),
        required=False,
        source=search_base_uid_source,
    )


@implementer(ITagsPortlet)
class Assignment(base.Assignment):

    def __init__(self,
                 header=u"",
                 maxsize=Decimal(2.0),
                 minsize=Decimal(0.7),
                 footer=u"",
                 search_base_uid=5):

        self.header = header
        self.maxsize = maxsize
        self.minsize = minsize
        self.footer = footer
        self.search_base_uid = search_base_uid

    @property
    def title(self):
        """
        This property is used to give the title of the portlet in the "manage
        portlets" screen.

        Here, we use the title that the user gave or static string if
        title not defined.

        """
        return self.header or _(u'portlet_tags', default=u"Tag Cloud")


class Renderer(base.Renderer):

    _template = ViewPageTemplateFile('tags.pt')

    @memoizedproperty
    def search_base_context(self):
        search_base_path = uuidToObject(self.data.search_base_uid)
        if search_base_path is not None:
            search_base_path = '/'.join(search_base_path.getPhysicalPath())

        if search_base_path:
            portal = find_ploneroot(self.context)
            search_base = '/'.join(search_base_path.split('/')[2:])
            return portal.unrestrictedTraverse(
                search_base.lstrip('/')
            )

        return find_site(self.context, as_url=False)

    @memoizedproperty
    def entries(self):
        query = {}
        query.update(self.request.get('contentFilter', {}))
        query['portal_type'] = 'collective.blog.blogentry'
        query['path'] = '/'.join(self.search_base_context.getPhysicalPath())

        cat = api.portal.get_tool('portal_catalog')
        return cat(**query)

    @memoizedproperty
    def subjects(self):
        subjects = {}
        for entrie in self.entries:
            for subject in entrie.Subject:
                if subject in subjects:
                    subjects[subject] += 1
                else:
                    subjects[subject] = 1

        result = []
        weight_list = sorted(subjects.values())
        if weight_list:
            minimal = weight_list[:1][0]
            maximal = weight_list[-1:][0]

            maxsize = float(self.data.maxsize)
            minsize = float(self.data.minsize)

            for subject, occurences in six.iteritems(subjects):
                try:
                    size = (float((maxsize * (occurences - minimal)))
                            / float((maximal - minimal)))
                except ZeroDivisionError:
                    size = 1
                if occurences <= minimal or size < minsize:
                    size = float(self.data.minsize)

                result.append({'title': subject, 'font_size': size})

            result.sort(key=lambda x: x['title'].lower())

        return result

    @memoizedproperty
    def subjects_root_url(self):
        context = self.search_base_context
        if context.layout == 'blog_listing':
            return context.absolute_url()

        return '/'.join((context.absolute_url(),
                         'blog_listing'))

    def render(self):
        return xhtml_compress(self._template())

    @property
    def available(self):
        """
        only show the portlet,

        when already tags are defined in this tagroot

        """

        if len(self.subjects) == 0:
            return False
        else:
            return True

    @property
    def has_header(self):
        return bool(self.data.header)

    @property
    def has_footer(self):
        return bool(self.data.footer)


class AddForm(base.AddForm):
    """
    Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.

    """
    schema = ITagsPortlet
    label = _(u"title_add_tags_portlet", default=u"Add Tag Cloud portlet")
    description = _(
        u"description_tags_portlet",
        default=u"This portlet displays a Tag Cloud " +
                u"for Tags within the current Tag Root."
    )

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    """
    Portlet edit form.

    This is registered with configure.zcml. The form_fields variable
    tells zope.formlib which fields to display.

    """
    schema = ITagsPortlet
    label = _(
        u"title_edit_tags_portlet",
        default=u"Edit Tag Cloud portlet"
    )
    description = _(
        u"description_tags_portlet",
        default=u"This portlet displays a Tag Cloud " +
                u"for Tags within the current Tag Root."
    )
