from collective.blog import _
from plone.app.z3cform.widget import AjaxSelectFieldWidget
from plone.autoform import directives
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from zope import schema
from zope.interface import provider
from zope.schema import Choice


@provider(IFormFieldProvider)
class IBlogTags(model.Schema):
    """Behavior adding the blog_tags field"""

    model.fieldset(
        "metadata",
        label=_("label_schema_metadata", default="Metadata"),
        fields=["blog_tags"],
    )
    blog_tags = schema.Tuple(
        title=_("label_blog_tags", default="Tags"),
        value_type=Choice(source="collective.blog.tags"),
        required=False,
        default=(),
        missing_value=(),
    )
    directives.widget(
        "blog_tags",
        AjaxSelectFieldWidget,
        vocabulary="collective.blog.tags",
        frontendOptions={
            "widget": "select",
        },
    )
