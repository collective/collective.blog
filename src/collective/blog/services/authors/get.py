from plone import api
from plone.restapi.interfaces import IExpandableElement
from plone.restapi.interfaces import ISerializeToJsonSummary
from plone.restapi.services import Service
from Products.ZCatalog.CatalogBrains import AbstractCatalogBrain
from typing import List
from zope.component import adapter
from zope.component import getMultiAdapter
from zope.interface import implementer
from zope.interface import Interface


DEFAULT_USER = "Plone"


@implementer(IExpandableElement)
@adapter(Interface, Interface)
class Authors:
    allowed_content_types = ("Post",)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def _get_authors_info(self, authors: List[str]) -> List[AbstractCatalogBrain]:
        """Given a list of uids, return a list of brains."""
        brains = api.content.find(portal_type="Author", UID=authors)
        return brains

    def _serialize_brains(self, brains: List[AbstractCatalogBrain]) -> List[dict]:
        """Serialize Authors information."""
        data = []
        for brain in brains:
            result = getMultiAdapter((brain, self.request), ISerializeToJsonSummary)()
            result["fullname"] = result["title"]
            data.append(result)
        return data

    def __call__(self, expand=True):
        result = {"authors": {"@id": f"{self.context.absolute_url()}/@authors"}}
        if not expand or self.context.portal_type not in self.allowed_content_types:
            return result

        portal_url = api.portal.get().absolute_url()
        default_authors = [
            {
                "@id": portal_url,
                "fullname": DEFAULT_USER,
                "description": "",
                "image_scales": None,
            }
        ]
        brains = self._get_authors_info(self.context.creators)
        result["authors"]["items"] = self._serialize_brains(brains) or default_authors
        return result


class AuthorsGet(Service):
    def reply(self):
        authors = Authors(self.context, self.request)
        return authors(expand=True)["authors"]
