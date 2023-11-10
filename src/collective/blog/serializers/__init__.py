from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.serializer.dxcontent import SerializeFolderToJson
from zope.component import getMultiAdapter


class BaseJSONSerializer(SerializeFolderToJson):
    portal_type: str = ""

    def __call__(self, version=None, include_items=True):
        context = self.context
        result = super().__call__(version, include_items)
        if context.portal_type == self.portal_type and context.preview_image_link:
            obj = context.preview_image_link.to_object
            result["preview_image_link"] = getMultiAdapter(
                (obj, self.request), ISerializeToJson
            )()
        return result
