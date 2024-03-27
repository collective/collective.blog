from collective.blog.vocabularies.tags import TermWithUrl
from plone.restapi.serializer.vocabularies import SerializeTermToJson
from zope.component import adapter
from zope.interface import Interface


@adapter(TermWithUrl, Interface)
class SerializeTermWithUrlToJson(SerializeTermToJson):
    """Include url in serialized term"""

    def __call__(self):
        result = super().__call__()
        result["url"] = self.context.url
        return result
