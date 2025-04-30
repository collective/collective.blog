from collective.blog.content.post import IPost
from plone import api
from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.serializer.dxcontent import SerializeFolderToJson
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface


@implementer(ISerializeToJson)
@adapter(IPost, Interface)
class PostAuthorsSerializer(SerializeFolderToJson):
    """Custom serializer for Award content type."""

    def __call__(self, **kwargs):
        result = super().__call__(**kwargs)
        brains = api.content.find(portal_type="Author", UID=self.context.creators)
        brains_by_uid = {brain.UID: brain for brain in brains}
        result["post_authors"] = authors = []

        for uid in self.context.creators:
            brain = brains_by_uid.get(uid)
            if brain:
                authors.append({
                    "title": brain.Title,
                    "url": brain.getURL(),
                })

        result["post_tags"] = tags = []
        tags_uids = [res["token"] for res in result["blog_tags"]]
        brains = api.content.find(portal_type="BlogTag", UID=tags_uids)
        brains_by_uid = {brain.UID: brain for brain in brains}

        for uid in tags_uids:
            brain = brains_by_uid.get(uid)
            if brain:
                tags.append({
                    "title": brain.Title,
                    "url": brain.getURL(),
                })

        return result
