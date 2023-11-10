from collective.blog.content.blog import IBlog
from collective.blog.serializers import BaseJSONSerializer
from plone.restapi.interfaces import ISerializeToJson
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface


@implementer(ISerializeToJson)
@adapter(IBlog, Interface)
class BlogJSONSerializer(BaseJSONSerializer):
    portal_type: str = "Blog"
