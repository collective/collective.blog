# -*- coding: utf-8 -*-
from __future__ import absolute_import
from zope import schema
from zope.interface import implementer

from AccessControl import ClassSecurityInfo
from Products.CMFCore import permissions
from plone import api
from plone.app.textfield import RichText
from plone.app.textfield.value import RichTextValue
from plone.autoform import directives as form
from plone.dexterity.browser import add
from plone.dexterity.browser import edit
from plone.dexterity.content import Container
from plone.registry.interfaces import IRegistry
from plone.supermodel import model
from plone.z3cform.fieldsets.utils import move
from z3c.form.interfaces import HIDDEN_MODE
from zope.component import getUtility

from .. import _
from ..interfaces import IBlogSettings


# Interface class; used to define content-type schema.
class IBlogEntry(model.Schema):
    """A Blog Entry."""

    form.omitted('summary')
    summary = RichText(
        title=_('label_summary', default=u'Summary'),
        description=_(
            'description_summary',
            default=u'Summary of the text for listings',
        ),
        required=False
    )

    show_images = schema.Bool(
        title=_('label_show_images', default=u'Show images as gallery'),
        description=_(
            'description_show_images',
            default=u'Decide if you want to '
                    u'show all uploaded images as gallery'
        ),
        default=False,
        required=False
    )


class EditForm(edit.DefaultEditForm):
    def update(self):
        # Get the fields
        self.portal_type = self.context.portal_type
        super(EditForm, self).updateFields()

        # Update them
        _add_edit_update(self)

        # And finaly call form update once.
        super(EditForm, self).update()


class AddForm(add.DefaultAddForm):
    portal_type = 'collective.blog.blogentry'

    def update(self):
        # Get the fields
        super(AddForm, self).updateFields()

        # Update them
        _add_edit_update(self)

        # And finaly call form update once.
        super(AddForm, self).update()


class AddView(add.DefaultAddView):
    form = AddForm


def _add_edit_update(self):
    # Flatten group fields.
    fields = {}
    for k, v in self.fields.items():
        fields[k] = v

    for group in self.groups:
        for k, v in group.fields.items():
            fields[k] = v

    # Set hidden fields
    fields['IDublinCore.description'].mode = HIDDEN_MODE

    registry = getUtility(IRegistry)
    show_lead_image = registry.forInterface(
        IBlogSettings, check=False).show_lead_image

    if not show_lead_image and 'ILeadImage.image' in fields:
        fields['ILeadImage.image'].mode = HIDDEN_MODE
        fields['ILeadImage.image_caption'].mode = HIDDEN_MODE

    # Move the text field after the title field
    move(self, 'IRichText.text', after='IDublinCore.title')

    # Set restricted fields
    restricted_fields = (
        'IDublinCore.creators',
        'IDublinCore.description',
        'IDublinCore.rights',
        'IAllowDiscussion.allow_discussion',
        'IExcludeFromNavigation.exclude_from_nav',
        'INextPreviousToggle.nextPreviousEnabled',
    )

    for rfield in restricted_fields:
        if rfield in fields:
            fields[rfield].read_permission = 'cmf.ModifyPortalContent'
            fields[rfield].write_permission = 'cmf.ModifyPortalContent'


@implementer(IBlogEntry)
class BlogEntry(Container):

    security = ClassSecurityInfo()

    @security.protected(permissions.View)
    def Summary(self):
        if not isinstance(self.summary, RichTextValue):
            return None

        # this is a CMF accessor, so should return utf8-encoded
        return self.summary.output.encode('utf-8') or ''

    @security.public
    def canSetDefaultPage(self):
        return False


#
# Eventhandlers
#
def on_object_modified(obj, event):
    _set_summary_and_description(obj)
    obj.reindexObject()


def on_object_added(obj, event):
    _set_summary_and_description(obj)
    obj.reindexObject()


#
# Internal helpers for the eventhandlers above
#
def _set_summary_and_description(obj):
    if obj.text is None:
        return

    try:
        obj.summary = RichTextValue(
            raw=obj.text.raw[0:obj.text.raw.index('<!--more-->')],
            mimeType=obj.text.mimeType,
            outputMimeType=obj.text.outputMimeType,
        )
    except ValueError:
        obj.summary = RichTextValue(
            raw=obj.text.raw[0:200],
            mimeType=obj.text.mimeType,
            outputMimeType=obj.text.outputMimeType,
        )

    portal_transforms = api.portal.get_tool('portal_transforms')
    datastream = portal_transforms.convertTo(
        'text/plain',
        obj.summary.output,
        mimetype='text/html')
    plain_text = datastream.getData()
    obj.setDescription(plain_text + '...')
