from collective.blog.content.author import IAuthor
from collective.blog.serializers import BaseJSONSerializer
from plone.restapi.interfaces import ISerializeToJson
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface


@implementer(ISerializeToJson)
@adapter(IAuthor, Interface)
class AuthorJSONSerializer(BaseJSONSerializer):
    portal_type: str = "Author"
