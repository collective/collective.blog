from collective.blog import _
from plone.app.z3cform.widget import AjaxSelectFieldWidget
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.supermodel import model
from z3c.form.interfaces import IAddForm
from z3c.form.interfaces import IEditForm
from zope import schema
from zope.interface import implementer
from zope.interface import Interface


class IPost(Interface):
    """A Blog Post."""

    # Metadata Fieldset
    model.fieldset(
        "metadata",
        label=_("label_schema_metadata", default="Metadata"),
        fields=["creators", "contributors", "rights"],
    )

    creators = schema.Tuple(
        title=_("label_authors", "Authors"),
        description=_(
            "help_authors",
            default="Persons responsible for creating the content of "
            "this post. Please enter a list of user names, one "
            "per line. The principal creator should come first.",
        ),
        value_type=schema.TextLine(),
        required=False,
        missing_value=(),
    )
    # Use Authors vocabulary
    directives.widget(
        "creators", AjaxSelectFieldWidget, vocabulary="collective.blog.authors"
    )

    contributors = schema.Tuple(
        title=_("contributors", "Contributors"),
        description=_(
            "help_contributors",
            default="The names of people that have contributed "
            "to this item. Each contributor should "
            "be on a separate line.",
        ),
        value_type=schema.TextLine(),
        required=False,
        missing_value=(),
    )
    directives.widget(
        "contributors", AjaxSelectFieldWidget, vocabulary="plone.app.vocabularies.Users"
    )

    rights = schema.Text(
        title=_("label_copyrights", default="Rights"),
        description=_(
            "help_copyrights",
            default="Copyright statement or other rights information on this " "item.",
        ),
        required=False,
    )

    directives.omitted("creators", "contributors", "rights")
    directives.no_omit(IEditForm, "creators", "contributors", "rights")
    directives.no_omit(IAddForm, "creators", "contributors", "rights")


@implementer(IPost)
class Post(Container):
    """A Blog Post."""
