from collective.blog.content.post import IPost
from collective.blog.serializers import BaseJSONSerializer
from plone.restapi.interfaces import ISerializeToJson
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface


@implementer(ISerializeToJson)
@adapter(IPost, Interface)
class PostJSONSerializer(BaseJSONSerializer):
    portal_type: str = "Post"
