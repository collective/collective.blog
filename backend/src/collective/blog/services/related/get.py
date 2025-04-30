from plone import api
from plone.restapi.services import Service


class GetRelated(Service):
    allowed_content_types = ("Post",)

    def reply(self):
        context = self.context
        blog_uid = context.blog_uid()

        if context.portal_type not in self.allowed_content_types:
            return

        if blog_uid:
            catalog = api.portal.get_tool("portal_catalog")

            brains = catalog.unrestrictedSearchResults(
                blog_uid=blog_uid, portal_type="Post"
            )

            for brain in brains:
                if brain.UID == context.UID():
                    continue

        return
